"""811 Vision AR edge server. Run: ./run.sh"""
import json
from collections import deque
from pathlib import Path

import cv2
import numpy as np
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, StreamingResponse

from edge.tags import FOCAL_PX_AT_1920, detect, survey
from edge.vision import ScanError, scan

app = FastAPI()

# ponytail: hand-written file stands in for the published revision; SQLite revisions in Phase 3.
MAP_FILE = Path(__file__).parent.parent / "sample_data" / "map.json"


def latest_map() -> dict | None:
    return json.loads(MAP_FILE.read_text()) if MAP_FILE.exists() else None


@app.get("/api/v1/status")
def status():
    m = latest_map()
    return {"ok": True, "published_revision": m and m["map_revision"]}


@app.get("/api/v1/maps/latest")
def maps_latest():
    m = latest_map()
    if m is None:
        raise HTTPException(404, "no published map")
    return m


_surveys: deque = deque(maxlen=15)  # recent live-view measurements, median-smoothed
_last_frame: dict = {}  # newest raw camera frame, for scanning


# Same state rules the phone uses (one source of truth).
_RULES = {j["id"]: {e["color"]: e["cover_in"] for e in j["entries"]}
          for j in json.loads((Path(__file__).parent.parent / "ios/App/jurisdictions.json").read_text())["jurisdictions"]}
MAX_ANCHOR_ERROR_PX = 25  # at 1920 px width; knob. Larger = more tolerant of bumped tags
_BGR = {"red": (40, 40, 230), "yellow": (0, 220, 255), "orange": (0, 130, 255), "blue": (230, 90, 20),
        "green": (60, 200, 40), "purple": (200, 40, 160), "pink": (180, 105, 255), "white": (255, 255, 255)}


def _draw_ar(img: np.ndarray, tags: dict, m: dict, state: str, scale: float | None = None) -> None:
    """Draw the published map on the camera frame: ground lines, plus pipes at SIMULATED depth
    (state minimum-cover rule, same as the phone). Needs all 4 anchors for the camera pose."""
    seen = [a for a in m["anchors"] if int(a["id"][1:]) - 1 in tags]
    if len(seen) < 4 or not m["utilities"]:
        return
    h, w = img.shape[:2]
    f = FOCAL_PX_AT_1920 * w / 1920
    k = np.float64([[f, 0, w / 2], [0, f, h / 2], [0, 0, 1]])
    ok, rvec, tvec = cv2.solvePnP(np.float64([a["position_m"] for a in seen]),
                                  np.float64([tags[int(a["id"][1:]) - 1].mean(axis=0) for a in seen]),
                                  k, None, flags=cv2.SOLVEPNP_IPPE)
    if not ok:
        return
    # Anchors moved since the survey? Then the pose is wrong and anything drawn would mislead.
    # Spec 10: flag it, never silently adopt new coordinates.
    obj, pix = np.float64([a["position_m"] for a in seen]), np.float64([tags[int(a["id"][1:]) - 1].mean(axis=0) for a in seen])
    error_px = np.linalg.norm(cv2.projectPoints(obj, rvec, tvec, k, None)[0].reshape(-1, 2) - pix, axis=1).max()
    if error_px > MAX_ANCHOR_ERROR_PX:
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


def _frames(index: int, state: str, scale: float | None):
    cam = cv2.VideoCapture(index)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    size_m = latest_map()["anchors"][0]["size_m"]
    try:
        while True:
            ok, img = cam.read()
            if not ok:
                break
            _last_frame["img"] = img.copy()
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
            _, jpg = cv2.imencode(".jpg", cv2.resize(img, (960, 540)))
            yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + jpg.tobytes() + b"\r\n"
    finally:
        cam.release()


@app.get("/camera")
def camera(index: int = 0, state: str = "WI", scale: float | None = None):
    """Supervisor aiming aid for the overhead scan (MJPEG). Not part of the worker app."""
    if scale is not None and not 0 < scale <= 1:
        raise HTTPException(422, "scale must be in (0, 1], e.g. 0.1 for 1:10")
    _surveys.clear()
    return StreamingResponse(_frames(index, state, scale), media_type="multipart/x-mixed-replace; boundary=frame")


def _measured_anchors() -> dict[str, list[float]]:
    if not _surveys:
        raise HTTPException(409, "no measurement yet: open /camera with A1 and A2 in view")
    # A tag may fail to decode in a few frames; keep it if seen in at least half of them.
    names = sorted(n for n in set().union(*_surveys) if 2 * sum(n in s for s in _surveys) >= len(_surveys))
    return {n: [round(float(np.median([s[n][i] for s in _surveys if n in s])), 3) for i in (0, 1)] for n in names}


def _save_anchors(m: dict, anchors: dict[str, list[float]]):
    missing = [a["id"] for a in m["anchors"] if a["id"] not in anchors]
    if missing:
        raise HTTPException(409, f"not saved: {missing} not in camera view")
    for a in m["anchors"]:
        a["position_m"] = anchors[a["id"]] + [0.0]
    m["map_revision"] += 1  # phones reload on revision change
    MAP_FILE.write_text(json.dumps(m, indent=2))


# ponytail: the two endpoints below change state on GET so they work from a browser bar;
# make them supervisor-only POST in Phase 3.
@app.get("/api/v1/survey")
def survey_anchors(save: bool = False):
    """Anchor layout measured by the live view (keep /camera open). ?save=true writes it into the map."""
    anchors = _measured_anchors()
    if save:
        _save_anchors(latest_map(), anchors)
    return {"anchors_m": anchors, "frames": len(_surveys), "saved": save}


@app.get("/api/v1/mock")
def mock_map(depth_m: float = 0.5, include_scan: bool = False):
    """Publish a MOCK utility map sized to the webcam-surveyed anchor area (keep /camera open).
    Mock lines are synthetic layout evidence. Their depth is display-only and labeled hypothetical;
    depth_m stays null (spec safety rule 2). ?include_scan=true adds paint seen by the camera."""
    anchors = _measured_anchors()
    xy = np.array(list(anchors.values()))
    (x0, y0), (w, h) = xy.min(axis=0), np.ptp(xy, axis=0)

    def at(u, v):  # fraction of the anchor area -> site meters
        return [round(float(x0 + u * w), 3), round(float(y0 + v * h), 3), 0.0]

    mock = [
        ("electric", "red", [at(0.15, 0.30), at(0.85, 0.30)]),
        ("gas", "yellow", [at(0.15, 0.80), at(0.85, 0.55)]),
        ("water", "blue", [at(0.50, 0.15), at(0.50, 0.50), at(0.85, 0.50)]),
    ]
    utilities = [{
        "utility_class": cls, "marking_color": color,
        "surface_marking": None,
        "uploaded_layout": {"centerline_m": line, "source_file": "MOCK (generated)", "registration_status": "registered_unreviewed"},
        "depth_m": None, "depth_status": "unknown",
        "display_depth_m": depth_m, "display_depth_status": "hypothetical",
        "evidence_relationship": "registered_unreviewed",
        "excavation_clearance_authorized": False,
    } for cls, color, line in mock]
    if include_scan:
        try:
            utilities += scan(_last_frame["img"], {k: tuple(v) for k, v in anchors.items()})[0]
        except ScanError as e:
            raise HTTPException(409, f"scan rejected: {e}")
    for i, u in enumerate(utilities):
        u["utility_id"] = f"U-{i + 1:03d}"

    m = latest_map()
    m["schema_version"] = "1.1"  # adds display_depth_m / display_depth_status
    m["map_status"] = "published_demonstration_only"
    m["utilities"] = utilities
    m["model_scale"] = 1.0
    _save_anchors(m, anchors)
    return {"published_revision": m["map_revision"], "anchors_m": anchors, "utilities": len(utilities)}


SAMPLE_DIR = MAP_FILE.parent
MAX_UPLOAD = 20 * 1024 * 1024


@app.post("/api/v1/scan")
async def scan_upload(request: Request, model_scale: float = 1.0):
    """Upload an overhead picture (raw image bytes as the body). It is scanned against the stored
    anchor positions and published as a new revision. model_scale < 1 marks a scale model
    (0.1 = 1:10): phones scale tolerance zones, depths, and length labels to match.
    ponytail: no supervisor auth yet; private LAN only. Add a token before any real use."""
    body = await request.body()
    if not 0 < len(body) <= MAX_UPLOAD:
        raise HTTPException(413, "image must be 1 byte to 20 MB")
    if not 0 < model_scale <= 1:
        raise HTTPException(422, "model_scale must be in (0, 1]")
    img = cv2.imdecode(np.frombuffer(body, np.uint8), cv2.IMREAD_COLOR)
    if img is None:
        raise HTTPException(415, "not a readable image (JPEG or PNG)")
    m = latest_map()
    try:
        utilities, preview = scan(img, {a["id"]: tuple(a["position_m"][:2]) for a in m["anchors"]})
    except ScanError as e:
        raise HTTPException(409, f"scan rejected: {e}")
    cv2.imwrite(str(SAMPLE_DIR / "scan_source.jpg"), img)  # spec: keep the source image
    cv2.imwrite(str(SAMPLE_DIR / "scan_preview.jpg"), preview)
    m["schema_version"] = "1.2"  # adds model_scale
    m["utilities"] = utilities
    m["model_scale"] = model_scale
    m["map_revision"] += 1
    MAP_FILE.write_text(json.dumps(m, indent=2))
    return {"published_revision": m["map_revision"], "model_scale": model_scale,
            "utilities": [{"id": u["utility_id"], "color": u["marking_color"], "class": u["utility_class"]} for u in utilities]}


@app.get("/api/v1/scan/preview")
def scan_preview():
    path = SAMPLE_DIR / "scan_preview.jpg"
    if not path.exists():
        raise HTTPException(404, "no scan yet")
    return FileResponse(path, headers={"Cache-Control": "no-store"})


@app.get("/", response_class=HTMLResponse)
def supervisor_page():
    return (Path(__file__).parent / "supervisor.html").read_text()
