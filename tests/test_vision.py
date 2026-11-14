"""Check: synthetic overhead photo (known tags + paint, perspective-skewed) -> scan recovers
the paint lines within 3 cm. Run: .venv/bin/python tests/test_vision.py"""
import sys
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent))
from edge.tags import tag_image
from edge.vision import ScanError, scan

ANCHORS = {"A1": (0.0, 0.0), "A2": (2.0, 0.0), "A3": (2.0, 2.0), "A4": (0.0, 2.0)}
S, PAD = 300, 0.4  # synthetic px per meter, border around site


def px(x, y):  # site meters -> synthetic top-down pixel (y up -> row down)
    return round((x + PAD) * S), round((2 + PAD - y) * S)


def make_photo(tags=4):
    side = round((2 + 2 * PAD) * S)
    rng = np.random.default_rng(0)
    ground = rng.normal(120, 12, (side, side, 3)).clip(0, 255).astype(np.uint8)  # noisy gray dirt
    for i, (x, y) in enumerate(list(ANCHORS.values())[:tags]):
        t = cv2.cvtColor(cv2.resize(tag_image(i, 300), (40, 40), interpolation=cv2.INTER_AREA), cv2.COLOR_GRAY2BGR)
        cx, cy = px(x, y)
        ground[cy - 20:cy + 20, cx - 20:cx + 20] = t
    cv2.line(ground, px(0.3, 0.7), px(1.7, 0.7), (30, 30, 220), 12)  # red, 4 cm wide
    cv2.line(ground, px(0.4, 1.0), px(1.5, 1.8), (30, 220, 230), 12)  # yellow diagonal
    # Skewed camera view
    src = np.float32([[0, 0], [side, 0], [side, side], [0, side]])
    dst = np.float32([[90, 40], [side - 60, 0], [side, side - 30], [20, side - 80]])
    return cv2.warpPerspective(ground, cv2.getPerspectiveTransform(src, dst), (side, side))


def ends(u):
    line = u["surface_marking"]["centerline_m"]
    return sorted([tuple(line[0][:2]), tuple(line[-1][:2])])


utilities, _ = scan(make_photo(), ANCHORS)
by_color = {u["marking_color"]: u for u in utilities}
assert set(by_color) == {"red", "yellow"}, f"found {[u['marking_color'] for u in utilities]}"
for color, truth in {"red": [(0.3, 0.7), (1.7, 0.7)], "yellow": [(0.4, 1.0), (1.5, 1.8)]}.items():
    for got, want in zip(ends(by_color[color]), truth):
        err = np.hypot(got[0] - want[0], got[1] - want[1])
        assert err < 0.03, f"{color} end {got} is {err:.3f} m from {want}"
assert all(u["depth_m"] is None and u["depth_status"] == "unknown" for u in utilities)

try:
    scan(make_photo(tags=3), ANCHORS)
    raise AssertionError("scan with 3 anchors must be rejected")
except ScanError:
    pass
print("ok: scan recovers paint lines within 3 cm, rejects missing anchors")

# Survey: anchor layout measured from one photo taken by a tilted pinhole camera.
from edge.tags import FOCAL_PX_AT_1920, survey


def pinhole_photo(tag_m=0.15, ppm=500):
    side = round(2.8 * ppm)  # top-down canvas, site origin 0.4 m in from the corner
    ground = np.full((side, side, 3), 120, np.uint8)
    full = round(tag_m * 4 / 3 * ppm)  # printed image = black square * 4/3
    for i, (x, y) in enumerate(ANCHORS.values()):
        tag = cv2.cvtColor(cv2.resize(tag_image(i, 600), (full, full), interpolation=cv2.INTER_AREA), cv2.COLOR_GRAY2BGR)
        cx, cy = round((x + 0.4) * ppm), round((2.4 - y) * ppm)
        ground[cy - full // 2:cy - full // 2 + full, cx - full // 2:cx - full // 2 + full] = tag
    # Camera above site center, tilted 12 deg; height chosen so the site fills the view whatever
    # the focal length knob is. World: x right, y up (site), z up.
    height = 3.2 * FOCAL_PX_AT_1920 / 1360
    k = np.float64([[FOCAL_PX_AT_1920, 0, 960], [0, FOCAL_PX_AT_1920, 540], [0, 0, 1]])
    tilt = np.radians(12)
    r = np.float64([[1, 0, 0], [0, -np.cos(tilt), -np.sin(tilt)], [0, np.sin(tilt), -np.cos(tilt)]])
    tvec = -r @ np.float64([1.0, 1.0 - height * np.tan(tilt), height])
    world_to_img = k @ np.column_stack([r[:, 0], r[:, 1], tvec])  # ground plane z = 0
    canvas_to_world = np.float64([[1 / ppm, 0, -0.4], [0, -1 / ppm, 2.4], [0, 0, 1]])
    return cv2.warpPerspective(ground, world_to_img @ canvas_to_world, (1920, 1080))


measured = survey(pinhole_photo(), 0.15)
for name, want in ANCHORS.items():
    err = np.hypot(measured[name][0] - want[0], measured[name][1] - want[1])
    assert err < 0.04, f"survey {name}: {measured[name]} is {err:.3f} m from {want}"
print("ok: survey measures anchor layout within 4 cm (2%)", measured)
