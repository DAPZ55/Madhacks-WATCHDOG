"""811 Vision AR edge server. Mac dev: ./run.sh   UNO Q: systemd user service (edge/vision811.service).

Workers (phones) only read:   GET /api/v1/maps/latest, /api/v1/status
Admin panel (GET /) drives:   upload or capture -> candidate -> review -> publish
ponytail: no admin login (owner's choice for the demo); private site Wi-Fi only.
          Add a token check on every POST before any real use.
"""
import json
import os
import socket
import subprocess
import sys
import threading
import time
from collections import deque
from pathlib import Path

import cv2
import numpy as np
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import FileResponse, HTMLResponse, StreamingResponse

from edge.tags import FOCAL_PX_AT_1920, detect, survey
from edge.vision import ScanError, scan

app = FastAPI()
ROOT = Path(__file__).parent.parent
DATA = ROOT / "sample_data"
MAP_FILE = DATA / "map.json"
HISTORY = DATA / "history"  # one immutable file per published revision
CANDIDATE = DATA / "candidate.json"  # scanned, waiting for the operator's approve/reject
MAX_UPLOAD = 20 * 1024 * 1024
STARTED = time.time()


# ---------- map storage ----------

def latest_map() -> dict | None:
    return json.loads(MAP_FILE.read_text()) if MAP_FILE.exists() else None


def _publish(m: dict, note: str) -> int:
    """Every change to what phones see goes through here: new revision number, history copy,
    atomic replace (a power cut mid-write must not corrupt the published map)."""
    m["map_revision"] += 1
    m["published_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
    m["publish_note"] = note
    text = json.dumps(m, indent=2)
    HISTORY.mkdir(exist_ok=True)
    (HISTORY / f"rev_{m['map_revision']:05d}.json").write_text(text)
    tmp = MAP_FILE.with_suffix(".tmp")
    tmp.write_text(text)
    os.replace(tmp, MAP_FILE)
    return m["map_revision"]


def _anchor_xy(m: dict) -> dict[str, tuple]:
    return {a["id"]: tuple(a["position_m"][:2]) for a in m["anchors"]}


@app.get("/api/v1/maps/latest")
def maps_latest():
    m = latest_map()
    if m is None:
        raise HTTPException(404, "no published map")
    m["site_mode"] = _mode()   # added at reply time, not stored: they describe now, not the revision
    m["alerts"] = _alerts()
    return m


@app.get("/api/v1/maps/{revision}")
def maps_revision(revision: int):
    path = HISTORY / f"rev_{revision:05d}.json"
    if not path.exists():
        raise HTTPException(404, f"revision {revision} not in history")
    return json.loads(path.read_text())


@app.get("/api/v1/history")
def history():
    out = []
    for path in sorted(HISTORY.glob("rev_*.json"), reverse=True)[:20]:
        m = json.loads(path.read_text())
        out.append({"revision": m["map_revision"], "published_at": m.get("published_at"),
                    "note": m.get("publish_note"), "utilities": len(m["utilities"]),
                    "model_scale": m.get("model_scale", 1.0)})
    return out


@app.post("/api/v1/rollback")
def rollback(revision: int):
    """Re-publish an old revision's content as a NEW revision. History is never rewritten."""
    old = maps_revision(revision)
    old["map_revision"] = latest_map()["map_revision"]
    return {"published_revision": _publish(old, f"rollback to revision {revision}")}


# ---------- camera ----------

_surveys: deque = deque(maxlen=15)  # live-view measurements, only for the on-screen distances
# One background thread owns the camera and keeps the newest frame here. Viewers, capture, and
# survey all read from it, so a stalled browser connection can never keep the camera to itself.
_cam: dict = {"thread": None, "frame": None, "seq": 0, "wanted": 0.0, "error": None}
CAMERA_IDLE_S = 5  # reader closes the camera this long after the last consumer


def _camera_index() -> int | None:
    """Which camera to open. Override with env VISION811_CAMERA=<index>.
    On the UNO Q some video nodes are the SoC's codec (qcom-venus), not a camera: skip them."""
    if os.environ.get("VISION811_CAMERA"):
        return int(os.environ["VISION811_CAMERA"])
    if not sys.platform.startswith("linux"):
        return 0
    for node in sorted(Path("/sys/class/video4linux").glob("video*"), key=lambda p: int(p.name[5:])):
        name = (node / "name").read_text().strip().lower()
        primary = (node / "index").read_text().strip() == "0"  # a UVC camera exposes 2 nodes; first is video
        if primary and "venus" not in name and "codec" not in name:
            return int(node.name[5:])
    return None


def _camera_reader(index: int):
    cam = cv2.VideoCapture(index)
    cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))  # 1080p at a usable rate over USB 2
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    cam.set(cv2.CAP_PROP_FPS, 10)  # every frame is JPEG-decoded; 30 fps pinned a core in Monitor mode for nothing
    try:
        warmup = 8  # auto-exposure still settling
        while time.time() - _cam["wanted"] < CAMERA_IDLE_S:
            ok, img = cam.read()
            if not ok:
                _cam["error"] = f"camera {index} stopped delivering frames"
                return
            if warmup:
                warmup -= 1
                continue
            _cam.update(frame=img, seq=_cam["seq"] + 1, error=None)
    finally:
        cam.release()
        _cam["frame"] = None


def _next_frame(after: int, timeout: float = 6.0) -> tuple[np.ndarray, int]:
    """Newest camera frame with sequence number > `after`. Starts the reader if needed."""
    index = _camera_index()
    if index is None:
        raise HTTPException(503, "no camera found: plug the webcam into the hub")
    _cam["wanted"] = time.time()
    if _cam["thread"] is None or not _cam["thread"].is_alive():
        _cam["error"] = None
        _cam["thread"] = threading.Thread(target=_camera_reader, args=(index,), daemon=True)
        _cam["thread"].start()
    deadline = time.time() + timeout
    while time.time() < deadline:
        frame, seq = _cam["frame"], _cam["seq"]
        if frame is not None and seq > after:
            return frame.copy(), seq
        if _cam["error"]:
            raise HTTPException(503, _cam["error"])
        time.sleep(0.01)
    raise HTTPException(503, "camera gave no frame in time")


def _grab(count: int = 1) -> list[np.ndarray]:
    """`count` distinct fresh frames."""
    frames, seq = [], _cam["seq"]
    for _ in range(count):
        frame, seq = _next_frame(seq)
        frames.append(frame)
    return frames


# Same state rules the phone uses (one source of truth).
_RULES = {j["id"]: {e["color"]: e["cover_in"] for e in j["entries"]}
          for j in json.loads((ROOT / "ios/App/jurisdictions.json").read_text())["jurisdictions"]}
MAX_ANCHOR_ERROR_PX = 25  # at 1920 px width; knob. Larger = more tolerant of bumped tags
_BGR = {"red": (40, 40, 230), "yellow": (0, 220, 255), "orange": (0, 130, 255), "blue": (230, 90, 20),
        "green": (60, 200, 40), "purple": (200, 40, 160), "pink": (180, 105, 255), "white": (255, 255, 255)}


def _camera_pose(tags: dict, m: dict, w: int, h: int):
    """Camera pose from the anchor tags, plus how far (px) the tags sit from where the map says they
    should be. Needs every anchor in view. Returns (rvec, tvec, k, error_px) or None."""
    seen = [a for a in m["anchors"] if int(a["id"][1:]) - 1 in tags]
    if len(seen) < 4:
        return None
    f = FOCAL_PX_AT_1920 * w / 1920
    k = np.float64([[f, 0, w / 2], [0, f, h / 2], [0, 0, 1]])
    obj = np.float64([a["position_m"] for a in seen])
    pix = np.float64([tags[int(a["id"][1:]) - 1].mean(axis=0) for a in seen])
    ok, rvec, tvec = cv2.solvePnP(obj, pix, k, None, flags=cv2.SOLVEPNP_IPPE)
    if not ok:
        return None
    error_px = float(np.linalg.norm(cv2.projectPoints(obj, rvec, tvec, k, None)[0].reshape(-1, 2) - pix, axis=1).max())
    return rvec, tvec, k, error_px


def _draw_ar(img: np.ndarray, tags: dict, m: dict, state: str, scale: float | None = None) -> None:
    """Draw the published map on the camera frame: ground lines, plus pipes at SIMULATED depth
    (state minimum-cover rule, same as the phone). Needs all 4 anchors for the camera pose."""
    h, w = img.shape[:2]
    pose = _camera_pose(tags, m, w, h)
    if pose is None or not m["utilities"]:
        return
    rvec, tvec, k, error_px = pose
    # Anchors moved since the survey? Then the pose is wrong and anything drawn would mislead.
    # Spec 10: flag it, never silently adopt new coordinates.
    if error_px > MAX_ANCHOR_ERROR_PX * w / 1920:
        cv2.rectangle(img, (0, h - 70), (w, h), (0, 0, 220), -1)
        cv2.putText(img, f"ANCHORS MOVED ({error_px:.0f} px off map). Overlay hidden. Re-survey the site.",
                    (30, h - 22), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (255, 255, 255), 3, cv2.LINE_AA)
        return

    def project(pts):
        return cv2.projectPoints(np.float64(pts), rvec, tvec, k, None)[0].reshape(-1, 2).astype(np.int32)

    scale = scale or m.get("model_scale", 1.0)  # explicit choice wins over the map's own scale
    drawn, curtains = [], img.copy()
    for u in m["utilities"]:
        path = ((u.get("uploaded_layout") or u.get("surface_marking")) or {}).get("centerline_m") or []
        if len(path) < 2:
            continue
        color = _BGR.get(u["marking_color"], (255, 255, 255))
        cover_in = _RULES.get(state, {}).get(u["marking_color"])
        depth = cover_in * 0.0254 if cover_in else u.get("display_depth_m")
        ground = project(path)
        pipe = project(np.float64(path) - [0, 0, depth * scale]) if depth else None
        if pipe is not None:
            for i in range(len(ground) - 1):  # see-through curtain from ground line down to pipe
                cv2.fillPoly(curtains, [np.array([ground[i], ground[i + 1], pipe[i + 1], pipe[i]])], color)
        drawn.append((u, color, ground, pipe, cover_in))
    img[:] = cv2.addWeighted(curtains, 0.3, img, 0.7, 0)
    for u, color, ground, pipe, cover_in in drawn:
        cv2.polylines(img, [ground], False, (255, 255, 255), 9, cv2.LINE_AA)
        cv2.polylines(img, [ground], False, color, 4, cv2.LINE_AA)
        if pipe is not None:
            cv2.polylines(img, [pipe], False, (0, 0, 0), 16, cv2.LINE_AA)
            cv2.polylines(img, [pipe], False, color, 11, cv2.LINE_AA)
        text = f"{u['utility_id']} {u['utility_class']}" + (f" ~{cover_in:.0f} in" if cover_in else "")
        at = (min(max(int(ground[0][0]) + 12, 10), w - 620), min(max(int(ground[0][1]) - 14, 40), h - 90))  # keep on screen
        cv2.putText(img, text, at, cv2.FONT_HERSHEY_SIMPLEX, 1.1, (0, 0, 0), 7, cv2.LINE_AA)
        cv2.putText(img, text, at, cv2.FONT_HERSHEY_SIMPLEX, 1.1, (255, 255, 255), 2, cv2.LINE_AA)
    note = f"SIMULATED DEPTH ({state} minimum cover, drawn 1:{1 / scale:.0f}). Not measured. Rev {m['map_revision']}"
    cv2.rectangle(img, (0, h - 70), (w, h), (0, 110, 255), -1)
    cv2.putText(img, note, (30, h - 22), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (255, 255, 255), 3, cv2.LINE_AA)


def _annotate(img: np.ndarray, state: str, scale: float | None) -> bytes:
    """Draw anchors, distances, and the published map on a camera frame. Returns a 960x540 JPEG."""
    size_m = latest_map()["anchors"][0]["size_m"]
    tags = detect(img)
    _draw_ar(img, tags, latest_map(), state, scale)
    for tag_id, corners in tags.items():  # outline anchors so aiming is easy
        cv2.polylines(img, [corners.astype("int32")], True, (0, 255, 0), 6)
        cv2.putText(img, f"A{tag_id + 1}", tuple(corners[0].astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 5)
    try:
        pos = survey(img, size_m, tags)
        _surveys.append(pos)
        mid = np.mean([c.mean(axis=0) for c in tags.values()], axis=0)
        ids = sorted(tags, key=lambda i: np.arctan2(*(tags[i].mean(axis=0) - mid)[::-1]))
        for a, b in zip(ids, ids[1:] + ids[:1]):  # distance along each edge of the anchor loop
            if a == b:
                continue
            pa, pb = tags[a].mean(axis=0), tags[b].mean(axis=0)
            d = np.hypot(*np.subtract(pos[f"A{a + 1}"], pos[f"A{b + 1}"]))
            cv2.line(img, tuple(pa.astype(int)), tuple(pb.astype(int)), (0, 255, 255), 3)
            cv2.putText(img, f"{d:.2f} m", tuple(((pa + pb) / 2).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255), 5)
    except ValueError:
        cv2.putText(img, "need A1 + A2 in view to measure", (40, 80), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)
    return cv2.imencode(".jpg", cv2.resize(img, (960, 540)))[1].tobytes()


def _frames(state: str, scale: float | None):
    seq = _cam["seq"]
    try:
        while True:
            img, seq = _next_frame(seq)
            yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + _annotate(img, state, scale) + b"\r\n"
    except HTTPException:
        return  # camera unplugged mid-stream: end the stream quietly


@app.get("/api/v1/snapshot")
def snapshot(state: str = "WI", scale: float | None = None):
    """One annotated camera frame (JPEG). For clients that cannot show an MJPEG stream."""
    if scale is not None and not 0 < scale <= 1:
        raise HTTPException(422, "scale must be in (0, 1], e.g. 0.1 for 1:10")
    return Response(_annotate(_grab(1)[-1], state, scale), media_type="image/jpeg", headers={"Cache-Control": "no-store"})


@app.get("/camera")
def camera(state: str = "WI", scale: float | None = None):
    """Live overhead view with anchors, distances, and the published map drawn on it (MJPEG)."""
    if scale is not None and not 0 < scale <= 1:
        raise HTTPException(422, "scale must be in (0, 1], e.g. 0.1 for 1:10")
    if _camera_index() is None:
        raise HTTPException(503, "no camera found: plug the webcam into the hub")
    return StreamingResponse(_frames(state, scale), media_type="multipart/x-mixed-replace; boundary=frame")


# ---------- operating mode ----------
# scan:    camera is aimed once, the site is surveyed and scanned, then the camera is not needed.
# monitor: camera stays aimed; the board keeps checking the anchors and warns every phone.
SETTINGS = DATA / "settings.json"
_monitor: dict = {"state": "off", "detail": "", "t": 0.0}
MONITOR_MESSAGES = {
    "anchors_moved": "Anchor tag moved. Overlay may be wrong. Re-survey needed.",
    "view_blocked": "Monitoring paused: camera cannot see all anchor tags.",
    "camera_offline": "Monitoring offline: overhead camera not available.",
}


def _mode() -> str:
    try:
        return json.loads(SETTINGS.read_text())["mode"]
    except (OSError, ValueError, KeyError):
        return "scan"


def _alerts() -> list[str]:
    """What every phone must be told right now. Monitoring that has silently stopped is itself an alert:
    never let phones assume someone is watching when nobody is."""
    if _mode() != "monitor":
        return []
    if time.time() - _monitor["t"] > 15:
        return [MONITOR_MESSAGES["camera_offline"]]
    return [MONITOR_MESSAGES[_monitor["state"]]] if _monitor["state"] in MONITOR_MESSAGES else []


def _watchdog():
    hidden_since = None
    while True:
        time.sleep(2)
        if _mode() != "monitor":
            _monitor.update(state="off", detail="")
            continue
        try:
            img = _grab(1)[-1]
            m = latest_map()
            tags = detect(img)
            pose = _camera_pose(tags, m, img.shape[1], img.shape[0])
            if pose is None:
                hidden_since = hidden_since or time.time()
                if time.time() - hidden_since > 6:  # someone walking through is not an alarm
                    seen = sum(int(a["id"][1:]) - 1 in tags for a in m["anchors"])
                    _monitor.update(state="view_blocked", detail=f"{seen} of {len(m['anchors'])} tags visible", t=time.time())
                continue
            hidden_since = None
            limit = MAX_ANCHOR_ERROR_PX * img.shape[1] / 1920
            moved = pose[3] > limit
            _monitor.update(state="anchors_moved" if moved else "ok", detail=f"tags {pose[3]:.0f} px from map (limit {limit:.0f})", t=time.time())
        except HTTPException as e:
            _monitor.update(state="camera_offline", detail=str(e.detail), t=time.time())
        except Exception as e:  # watchdog must never die silently
            _monitor.update(state="camera_offline", detail=f"{type(e).__name__}: {e}", t=time.time())


threading.Thread(target=_watchdog, daemon=True).start()


@app.post("/api/v1/mode")
def set_mode(mode: str):
    if mode not in ("scan", "monitor"):
        raise HTTPException(422, "mode must be scan or monitor")
    if mode == "monitor":
        # Refuse to promise monitoring the board cannot deliver.
        visible = _visible_tags()
        if len(visible["visible"]) < len(visible["needed"]):
            raise HTTPException(409, f"aim the camera first: {len(visible['visible'])} of {len(visible['needed'])} anchor tags visible")
    SETTINGS.write_text(json.dumps({"mode": mode}))
    _monitor.update(state="ok" if mode == "monitor" else "off", detail="", t=time.time())
    return {"mode": mode}


def _visible_tags() -> dict:
    # A tag at a steep angle or near the frame edge decodes in some frames and not others;
    # judging from one frame flickers. Readable = decoded in any of 5 frames.
    seen = set().union(*(detect(img) for img in _grab(5)))
    needed = [a["id"] for a in latest_map()["anchors"]]
    return {"needed": needed, "visible": [n for n in needed if int(n[1:]) - 1 in seen]}


@app.get("/api/v1/tags")
def visible_tags():
    """Which anchor tags the camera can read right now. For aiming before a scan."""
    return _visible_tags()


# ---------- anchor survey ----------

def _measured_anchors(frames: list | None = None) -> dict[str, list[float]]:
    """Anchor layout measured from a burst of camera frames (a fresh burst unless given)."""
    size_m = latest_map()["anchors"][0]["size_m"]
    surveys = []
    for img in frames or _grab(8):
        try:
            surveys.append(survey(img, size_m))
        except ValueError:
            pass
    if not surveys:
        raise HTTPException(409, "cannot measure: A1 and A2 must both be in camera view")
    # A tag may fail to decode in a few frames; keep it if seen in at least half of them.
    names = sorted(n for n in set().union(*surveys) if 2 * sum(n in s for s in surveys) >= len(surveys))
    return {n: [round(float(np.median([s[n][i] for s in surveys if n in s])), 3) for i in (0, 1)] for n in names}


def _set_anchors(m: dict, anchors: dict[str, list[float]]):
    missing = [a["id"] for a in m["anchors"] if a["id"] not in anchors]
    if missing:
        raise HTTPException(409, f"not saved: {missing} not in camera view")
    for a in m["anchors"]:
        a["position_m"] = anchors[a["id"]] + [0.0]


@app.get("/api/v1/survey")
def survey_read():
    return {"anchors_m": _measured_anchors()}


@app.post("/api/v1/survey")
def survey_save():
    """Measure the anchor tags with the camera and store their positions. Existing utilities were
    placed relative to the OLD anchor positions, so they are cleared: rescan after a re-survey."""
    anchors = _measured_anchors()
    m = latest_map()
    _set_anchors(m, anchors)
    m["utilities"] = []
    CANDIDATE.unlink(missing_ok=True)
    return {"published_revision": _publish(m, "anchors re-surveyed; utilities cleared"), "anchors_m": anchors}


# ---------- scan -> candidate -> review -> publish ----------

def _make_candidate(img: np.ndarray, model_scale: float, source: str, anchors: dict | None = None) -> dict:
    """`anchors`: freshly surveyed tag positions to scan against and to publish together with the result."""
    if not 0 < model_scale <= 1:
        raise HTTPException(422, "model_scale must be in (0, 1]")
    try:
        utilities, preview = scan(img, {k: tuple(v) for k, v in anchors.items()} if anchors else _anchor_xy(latest_map()))
    except ScanError as e:
        raise HTTPException(409, f"scan rejected: {e}")
    cv2.imwrite(str(DATA / "scan_source.jpg"), img)  # spec: keep the source image
    cv2.imwrite(str(DATA / "scan_preview.jpg"), preview)
    candidate = {"source": source, "scanned_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                 "model_scale": model_scale, "utilities": utilities, "anchors_m": anchors}
    CANDIDATE.write_text(json.dumps(candidate))
    return _candidate_summary(candidate)


def _candidate_summary(c: dict) -> dict:
    return {"source": c["source"], "scanned_at": c["scanned_at"], "model_scale": c["model_scale"],
            "includes_survey": bool(c.get("anchors_m")),
            "utilities": [{"id": u["utility_id"], "color": u["marking_color"], "class": u["utility_class"],
                           "points": len(u["surface_marking"]["centerline_m"])} for u in c["utilities"]]}


@app.post("/api/v1/scan")
async def scan_upload(request: Request, model_scale: float = 1.0):
    """Upload an overhead picture (raw image bytes as the body). It is scanned on this board against
    the stored anchor positions. Result is a CANDIDATE: nothing reaches phones until /publish.
    model_scale < 1 marks a scale model (0.1 = 1:10)."""
    body = await request.body()
    if not 0 < len(body) <= MAX_UPLOAD:
        raise HTTPException(413, "image must be 1 byte to 20 MB")
    img = cv2.imdecode(np.frombuffer(body, np.uint8), cv2.IMREAD_COLOR)
    if img is None:
        raise HTTPException(415, "not a readable image (JPEG or PNG)")
    return _make_candidate(img, model_scale, "uploaded picture")


@app.post("/api/v1/capture")
def scan_capture(model_scale: float = 1.0):
    """Same as /scan, but the picture comes from the overhead webcam."""
    return _make_candidate(_grab(1)[-1], model_scale, "overhead camera")


@app.post("/api/v1/scan_site")
def scan_site(model_scale: float = 1.0):
    """One-time scan: survey the anchor tags AND scan the markings from the same burst of frames, so
    the two always agree. After this is approved the camera is no longer needed."""
    frames = _grab(8)
    anchors = _measured_anchors(frames)
    missing = [a["id"] for a in latest_map()["anchors"] if a["id"] not in anchors]
    if missing:
        raise HTTPException(409, f"cannot scan: {missing} not in camera view")
    return _make_candidate(frames[-1], model_scale, "one-time site scan", anchors)


@app.get("/api/v1/candidate")
def candidate():
    if not CANDIDATE.exists():
        raise HTTPException(404, "no candidate waiting")
    return _candidate_summary(json.loads(CANDIDATE.read_text()))


@app.get("/api/v1/scan/preview")
def scan_preview():
    path = DATA / "scan_preview.jpg"
    if not path.exists():
        raise HTTPException(404, "no scan yet")
    return FileResponse(path, headers={"Cache-Control": "no-store"})


@app.post("/api/v1/publish")
def publish():
    """Operator approved the candidate: it becomes the map phones see."""
    if not CANDIDATE.exists():
        raise HTTPException(404, "no candidate waiting")
    c = json.loads(CANDIDATE.read_text())
    for u in c["utilities"]:
        u["surface_marking"]["operator_reviewed"] = True
    m = latest_map()
    m["schema_version"] = "1.2"
    if c.get("anchors_m"):
        _set_anchors(m, c["anchors_m"])
    m["utilities"] = c["utilities"]
    m["model_scale"] = c["model_scale"]
    revision = _publish(m, f"{c['source']}, {len(c['utilities'])} utilities, approved")
    CANDIDATE.unlink()
    return {"published_revision": revision}


@app.post("/api/v1/reject")
def reject():
    CANDIDATE.unlink(missing_ok=True)
    return {"ok": True}


@app.get("/api/v1/mock")
def mock_map(depth_m: float = 0.5):
    """Dev helper: publish a MOCK utility map sized to the surveyed anchor area. Mock lines are
    synthetic layout evidence; their depth is display-only and labeled hypothetical."""
    anchors = _measured_anchors()
    xy = np.array(list(anchors.values()))
    (x0, y0), (w, h) = xy.min(axis=0), np.ptp(xy, axis=0)

    def at(u, v):  # fraction of the anchor area -> site meters
        return [round(float(x0 + u * w), 3), round(float(y0 + v * h), 3), 0.0]

    mock = [("electric", "red", [at(0.15, 0.30), at(0.85, 0.30)]),
            ("gas", "yellow", [at(0.15, 0.80), at(0.85, 0.55)]),
            ("water", "blue", [at(0.50, 0.15), at(0.50, 0.50), at(0.85, 0.50)])]
    m = latest_map()
    _set_anchors(m, anchors)
    m["schema_version"] = "1.2"
    m["model_scale"] = 1.0
    m["utilities"] = [{
        "utility_id": f"U-{i + 1:03d}", "utility_class": cls, "marking_color": color,
        "surface_marking": None,
        "uploaded_layout": {"centerline_m": line, "source_file": "MOCK (generated)", "registration_status": "registered_unreviewed"},
        "depth_m": None, "depth_status": "unknown",
        "display_depth_m": depth_m, "display_depth_status": "hypothetical",
        "evidence_relationship": "registered_unreviewed",
        "excavation_clearance_authorized": False,
    } for i, (cls, color, line) in enumerate(mock)]
    return {"published_revision": _publish(m, "mock map")}


# ---------- status, power, page ----------

@app.get("/api/v1/status")
def status():
    m = latest_map()
    return {"ok": True, "host": socket.gethostname(), "uptime_s": round(time.time() - STARTED),
            "published_revision": m and m["map_revision"], "published_at": m and m.get("published_at"),
            "utilities": m and len(m["utilities"]), "model_scale": m and m.get("model_scale", 1.0),
            "camera": _camera_index() is not None, "camera_active": bool(_cam["thread"] and _cam["thread"].is_alive()),
            "candidate_waiting": CANDIDATE.exists(),
            "mode": _mode(), "monitor_state": _monitor["state"], "monitor_detail": _monitor["detail"], "alerts": _alerts()}


SITE_WIFI = "811-site"  # profile made by edge/setup_wifi.sh; SSID 811-Vision, board is 10.42.0.1


def _nm(*args: str) -> str:
    if not sys.platform.startswith("linux"):
        raise HTTPException(501, "network control only works on the UNO Q")
    return subprocess.run(["nmcli", *args], capture_output=True, text=True, timeout=30).stdout


def _wifi_profiles() -> list[str]:
    """Saved Wi-Fi profiles, most recently used first."""
    rows = [line.rsplit(":", 2) for line in _nm("-t", "-f", "NAME,TYPE,TIMESTAMP", "connection", "show").splitlines()]
    wifi = [(int(r[2] or 0), r[0]) for r in rows if len(r) == 3 and r[1] == "802-11-wireless"]
    return [name for _, name in sorted(wifi, reverse=True)]


@app.get("/api/v1/network")
def network():
    if not sys.platform.startswith("linux"):
        return {"supported": False}
    active = [line.rsplit(":", 1)[0] for line in _nm("-t", "-f", "NAME,TYPE", "connection", "show", "--active").splitlines()
              if line.endswith(":802-11-wireless")]
    configured = SITE_WIFI in _wifi_profiles()
    at_boot = configured and _nm("-g", "connection.autoconnect", "connection", "show", SITE_WIFI).strip() == "yes"
    return {"supported": True, "site_wifi_configured": configured, "own_network_at_boot": at_boot,
            "mode": "own_network" if SITE_WIFI in active else "joined" if active else "offline",
            "connected_to": active[0] if active else None,
            "addresses": [a for a in _nm("-g", "IP4.ADDRESS", "device", "show", "wlan0").replace("|", "\n").split() if a]}


def _switch_network(own: bool):
    """Runs after the HTTP reply has gone out, since the link the request came over is about to drop."""
    time.sleep(1.5)
    if own:
        _nm("connection", "up", SITE_WIFI)
        return
    for name in _wifi_profiles():
        if name != SITE_WIFI and "successfully" in _nm("connection", "up", name):
            return
    _nm("connection", "up", SITE_WIFI)  # hotspot not found: never leave the board unreachable


@app.post("/api/v1/network")
def network_switch(mode: str):
    """mode=own: broadcast the board's own Wi-Fi. mode=join: rejoin the last hotspot/router
    (falls back to own network if that fails). The caller's connection drops either way."""
    if mode not in ("own", "join"):
        raise HTTPException(422, "mode must be own or join")
    if SITE_WIFI not in _wifi_profiles():
        raise HTTPException(409, "own network not set up yet: run edge/setup_wifi.sh on the board")
    threading.Thread(target=_switch_network, args=(mode == "own",), daemon=True).start()
    return {"ok": True, "switching_to": mode}


@app.post("/api/v1/network/boot")
def network_boot(own: bool):
    """own=true: at power-on, if no known hotspot/router is in range, start the board's own Wi-Fi.
    Known networks keep priority, so the hotspot still wins when it is on."""
    if SITE_WIFI not in _wifi_profiles():
        raise HTTPException(409, "own network not set up yet: run edge/setup_wifi.sh on the board")
    _nm("connection", "modify", SITE_WIFI, "connection.autoconnect", "yes" if own else "no",
        "connection.autoconnect-priority", "-10")
    for name in _wifi_profiles():
        if name != SITE_WIFI:
            _nm("connection", "modify", name, "connection.autoconnect-priority", "10")
    return {"ok": True, "own_network_at_boot": own}


@app.post("/api/v1/power")
def power(action: str):
    """Clean shutdown or reboot of the board. Needs a one-time sudoers rule (see admin panel)."""
    if action not in ("poweroff", "reboot"):
        raise HTTPException(422, "action must be poweroff or reboot")
    if not sys.platform.startswith("linux"):
        raise HTTPException(501, "power control only works on the UNO Q")
    result = subprocess.run(["sudo", "-n", "systemctl", action], capture_output=True, text=True)
    if result.returncode != 0:
        raise HTTPException(501, "not permitted yet. One-time setup on the board: "
                                 "echo 'arduino ALL=(root) NOPASSWD: /usr/bin/systemctl poweroff, /usr/bin/systemctl reboot' "
                                 "| sudo tee /etc/sudoers.d/vision811-power")
    return {"ok": True, "action": action}


@app.get("/", response_class=HTMLResponse)
def admin_page():
    return (Path(__file__).parent / "admin.html").read_text()
