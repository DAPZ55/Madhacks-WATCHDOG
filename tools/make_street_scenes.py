"""Generate SYNTHETIC overhead street scenes with 811-style paint for the upload demo.
Not real imagery: procedural asphalt/sidewalk/lane lines + APWA-colored utility marks.
Anchor tags are drawn at the positions stored in sample_data/map.json, so a scan of the
picture lands on the real floor tags. Scenes are 1:10 scale models (1 m on the floor = 10 m).

Run: .venv/bin/python tools/make_street_scenes.py
Out: sample_data/streets/street_NN.jpg + street_NN.json (ground truth, site-frame meters)
"""
import json
import sys
from pathlib import Path

import cv2
import numpy as np

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
from edge.tags import tag_image
from tools import marking_symbols as sym
from edge.vision import MARGIN_M

PPM = 1000  # image pixels per floor meter
MODEL_SCALE = 0.1
PAINT = {  # BGR, saturated spray paint
    "red": (40, 40, 230), "yellow": (0, 220, 255), "orange": (0, 130, 255),
    "blue": (230, 90, 20), "green": (60, 200, 40), "purple": (200, 40, 160),
}
CLASS = {"red": "electric", "yellow": "gas", "orange": "communications",
         "blue": "water", "green": "sewer", "purple": "reclaimed_water"}
LETTER = {"red": "E", "yellow": "G", "orange": "T", "blue": "W", "green": "S", "purple": "RW"}

# Scenes are authored in u,v: fraction of image width/height, v down. Keep utility lines out of
# the tag boxes (around u 0.19/0.80, v 0.25/0.73): rows v 0.36-0.63 and columns u 0.28-0.71 are clear.
SCENES = [
    dict(title="Residential street", road="straight", center="white", hard=False, utilities=[
        ("red", [(0.04, 0.36), (0.96, 0.36)]),
        ("blue", [(0.05, 0.60), (0.95, 0.60)]),
        ("yellow", [(0.30, 0.64), (0.68, 0.41)]),
    ]),
    dict(title="Intersection", road="cross", center="white", hard=False, utilities=[
        ("green", [(0.50, 0.04), (0.50, 0.96)]),
        ("orange", [(0.04, 0.38), (0.44, 0.38), (0.44, 0.05)]),
        ("blue", [(0.05, 0.60), (0.95, 0.60)]),
    ]),
    dict(title="Service laterals", road="straight", center="white", hard=False, utilities=[
        ("red", [(0.05, 0.60), (0.50, 0.60), (0.70, 0.37), (0.96, 0.37)]),
        ("yellow", [(0.32, 0.04), (0.32, 0.96)]),
        ("purple", [(0.04, 0.42), (0.60, 0.42)]),
    ]),
    # Hard scenes: road paint that looks like utility paint. Classical color detection is fooled;
    # this is what the AI validator is for.
    dict(title="Double yellow + fire lane curb (hard)", road="straight", center="double_yellow", hard=True,
         red_curb=True, utilities=[
        ("yellow", [(0.05, 0.60), (0.95, 0.60)]),
        ("red", [(0.60, 0.04), (0.60, 0.96)]),
    ]),
    dict(title="Busy intersection (hard)", road="cross", center="double_yellow", hard=True, barrier=True,
         utilities=[
        ("green", [(0.52, 0.04), (0.52, 0.96)]),
        ("orange", [(0.04, 0.37), (0.96, 0.37)]),
        ("blue", [(0.30, 0.96), (0.30, 0.60), (0.96, 0.60)]),
        ("red", [(0.68, 0.04), (0.68, 0.34)]),
    ]),
]

# Scenes painted with real marking SYMBOLS (arrows, owner initials, sizes, offsets...) instead of bare
# lines. Output marks_NN.jpg. Each mark: (kind, color, points in u,v, text...). See marking_symbols.py.
MARK_SCENES = [
    dict(title="Line markings: owner initials, high-pressure gas, oversized water", road="straight", center="white", marks=[
        ("line", "red", [(0.04, 0.40), (0.96, 0.40)], "SRP"),
        ("line", "yellow", [(0.04, 0.60), (0.96, 0.60)], 'SWG 8" HP STL'),
        ("oversized", "blue", [(0.50, 0.04), (0.50, 0.96)], 'W 42"'),
    ]),
    dict(title="Conduit, buried splice, termination", road="cross", center="white", marks=[
        ("conduit", "orange", [(0.39, 0.04), (0.39, 0.96)], "USW DUCT"),
        ("splice", "green", [(0.61, 0.04), (0.61, 0.96)], 0.5),
        ("termination", "red", [(0.03, 0.50), (0.20, 0.50)], 'MF 4"'),
    ]),
    dict(title="Offset mark, corridor, no-conflict statements", road="straight", center="white", marks=[
        ("corridor", "purple", [(0.29, 0.41), (0.71, 0.41)], "SRP"),
        ("offset", "yellow", [(0.45, 0.62), (0.45, 0.50)], "SWG", "12'"),
        ("line", "blue", [(0.04, 0.60), (0.36, 0.60)], "W"),
        ("no_conflict", "orange", [(0.50, 0.065)], "MCI"),
        ("no_conflict", "red", [(0.50, 0.935)], "EPG"),
    ]),
]


def main():
    site = json.loads((ROOT / "sample_data" / "map.json").read_text())
    anchors = {a["id"]: a["position_m"][:2] for a in site["anchors"]}
    size_m = site["anchors"][0]["size_m"]
    xy = np.array(list(anchors.values()))
    x0, y1 = xy[:, 0].min() - MARGIN_M, xy[:, 1].max() + MARGIN_M
    w_m, h_m = np.ptp(xy[:, 0]) + 2 * MARGIN_M, np.ptp(xy[:, 1]) + 2 * MARGIN_M
    W, H = round(w_m * PPM), round(h_m * PPM)
    rng = np.random.default_rng(811)

    def px(u, v):
        return round(u * W), round(v * H)

    def to_site(u, v):
        return [round(float(x0 + u * w_m), 3), round(float(y1 - v * h_m), 3), 0.0]

    def texture(base, spread):
        """Speckled surface: per-pixel noise plus soft blotches."""
        blot = cv2.resize(rng.normal(0, spread, (H // 40, W // 40)).astype(np.float32), (W, H))
        return base + rng.normal(0, spread, (H, W)) + blot

    def dashed(img, pts, color, thick, dash_m, gap_m):
        for (ua, va), (ub, vb) in zip(pts, pts[1:]):
            a, b = np.float64(px(ua, va)), np.float64(px(ub, vb))
            length = np.linalg.norm(b - a)
            step, t = (dash_m + gap_m) * PPM, 0.0
            while t < length:
                p = a + (b - a) * t / length
                q = a + (b - a) * min(t + dash_m * PPM, length) / length
                cv2.line(img, tuple(p.astype(int)), tuple(q.astype(int)), color, thick, cv2.LINE_AA)
                t += step

    out = ROOT / "sample_data" / "streets"
    out.mkdir(parents=True, exist_ok=True)
    jobs = [(f"street_{n:02d}", sc) for n, sc in enumerate(SCENES, 1)] + \
           [(f"marks_{n:02d}", sc) for n, sc in enumerate(MARK_SCENES, 1)]
    for stem, scene in jobs:
        gray = texture(165, 7)  # concrete sidewalk everywhere, then carve grass and road
        gray[px(0, 0.13)[1]:px(0, 0.87)[1]] = texture(95, 6)[px(0, 0.13)[1]:px(0, 0.87)[1]]  # verge
        img = cv2.merge([gray, gray, gray]).clip(0, 255).astype(np.uint8)
        img[px(0, 0.13)[1]:px(0, 0.20)[1]] = (img[px(0, 0.13)[1]:px(0, 0.20)[1]] * [0.6, 0.95, 0.6]).astype(np.uint8)
        img[px(0, 0.80)[1]:px(0, 0.87)[1]] = (img[px(0, 0.80)[1]:px(0, 0.87)[1]] * [0.6, 0.95, 0.6]).astype(np.uint8)
        asphalt = cv2.merge([texture(62, 9)] * 3).clip(0, 255).astype(np.uint8)
        road = np.zeros((H, W), bool)
        road[px(0, 0.20)[1]:px(0, 0.80)[1]] = True
        if scene["road"] == "cross":
            road[:, px(0.34, 0)[0]:px(0.66, 0)[0]] = True
        for u in np.arange(0.0, 1.0, 0.09):  # sidewalk joints
            cv2.line(img, px(u, 0), px(u, 0.13), (120, 120, 120), 2)
            cv2.line(img, px(u, 0.87), px(u, 1), (120, 120, 120), 2)
        img[road] = asphalt[road]
        for _ in range(6):  # asphalt cracks
            p = np.float64([rng.uniform(0, W), rng.uniform(0.25, 0.75) * H])
            for _ in range(12):
                q = p + rng.normal(0, 35, 2)
                cv2.line(img, tuple(p.astype(int)), tuple(q.astype(int)), (38, 38, 38), 1, cv2.LINE_AA)
                p = q

        # Road paint (not utility marks)
        cross = scene["road"] == "cross"
        spans = [(0.0, 0.33), (0.67, 1.0)] if cross else [(0.0, 1.0)]
        for ua, ub in spans:
            if scene["center"] == "white":
                dashed(img, [(ua, 0.5), (ub, 0.5)], (235, 235, 235), 10, 0.10, 0.10)
            else:
                for dv in (-0.012, 0.012):
                    cv2.line(img, px(ua, 0.5 + dv), px(ub, 0.5 + dv), PAINT["yellow"], 9, cv2.LINE_AA)
        if cross:
            for v in np.arange(0.23, 0.78, 0.045):  # crosswalk bars
                cv2.rectangle(img, px(0.31, v), px(0.33, v + 0.025), (235, 235, 235), -1)
                cv2.rectangle(img, px(0.67, v), px(0.69, v + 0.025), (235, 235, 235), -1)
            cv2.circle(img, px(0.50, 0.50), 38, (45, 45, 45), -1)  # manhole
            cv2.circle(img, px(0.50, 0.50), 38, (25, 25, 25), 4)
        cv2.rectangle(img, px(0.90, 0.775), px(0.95, 0.80), (20, 20, 20), -1)  # storm drain
        if scene.get("red_curb"):
            cv2.line(img, px(0, 0.20), px(1, 0.20), (30, 30, 200), 16)
        if scene.get("barrier"):
            cv2.rectangle(img, px(0.74, 0.44), px(0.92, 0.47), PAINT["orange"], -1)

        # 811 utility marks: dashed spray lines + letter, with spray dropouts
        before = img.copy()
        truth = []
        for i, (kind, color, pts, *extra) in enumerate(scene.get("marks", []), 1):
            p = [np.float64(px(u, v)) for u, v in pts]
            args = (img, p, PAINT[color], *extra) if kind == "line" else (img, *p, PAINT[color], *extra)
            mark = getattr(sym, f"draw_{kind}")(*args)
            # pixel -> u,v -> site meters
            mark["points_m"] = [to_site(q[0] / W, q[1] / H) for q in mark.pop("points_px")]
            truth.append({"utility_id": f"U-{i:03d}", "marking_color": color, "utility_class": CLASS[color],
                          "text": " ".join(str(e) for e in extra if isinstance(e, str)), **mark})
        for i, (color, pts) in enumerate(scene.get("utilities", []), 1):
            dashed(img, pts, PAINT[color], 16, 0.06, 0.03)
            (ua, va), (ub, vb) = pts[0], pts[1]
            side = np.array([-(vb - va) * H, (ub - ua) * W])
            side = side / np.linalg.norm(side) * 130  # letter sits 13 cm (floor) off the line
            at = np.float64(px(ua + (ub - ua) * 0.25, va + (vb - va) * 0.25)) + side
            cv2.putText(img, LETTER[color], tuple(at.astype(int) - (12, -12)), cv2.FONT_HERSHEY_SIMPLEX, 1.1,
                        PAINT[color], 3, cv2.LINE_AA)
            truth.append({"utility_id": f"U-{i:03d}", "marking_color": color, "utility_class": CLASS[color],
                          "centerline_m": [to_site(u, v) for u, v in pts]})
        dropout = rng.random((H, W)) < 0.06
        img[dropout] = before[dropout]

        # Anchor tags on top, at the surveyed floor positions
        full = round(size_m * 4 / 3 * PPM)
        for t, (name, (ax, ay)) in enumerate(anchors.items()):
            tag = cv2.cvtColor(cv2.resize(tag_image(t, 600), (full, full), interpolation=cv2.INTER_AREA),
                               cv2.COLOR_GRAY2BGR)
            cx, cy = round((ax - x0) * PPM), round((y1 - ay) * PPM)
            img[cy - full // 2:cy - full // 2 + full, cx - full // 2:cx - full // 2 + full] = tag

        img = cv2.GaussianBlur(img, (3, 3), 0)
        cv2.imwrite(str(out / f"{stem}.jpg"), img, [cv2.IMWRITE_JPEG_QUALITY, 90])
        (out / f"{stem}.json").write_text(json.dumps({
            "title": scene["title"], "synthetic": True, "model_scale": MODEL_SCALE, "hard": scene.get("hard", False),
            "symbols": "marks" in scene,
            "note": "Hard scenes contain road paint that color detection mistakes for utility marks.",
            "utilities": truth,
        }, indent=2))
        print(f"{stem}.jpg  {W}x{H}  {scene['title']}  ({len(truth)} marks)")


if __name__ == "__main__":
    main()
