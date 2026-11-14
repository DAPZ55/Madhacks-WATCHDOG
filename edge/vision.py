"""One-time overhead scan: image -> utility polylines in site frame S (meters).

Usage:
  python -m edge.vision --image photo.jpg        # scan a saved photo
  python -m edge.vision --camera 0               # grab a 1080p still from the webcam, then scan
Writes sample_data/scan.json (candidate utilities, NOT published) and sample_data/scan_preview.jpg.
"""
import argparse
import json
from pathlib import Path

import cv2
import numpy as np

from edge.tags import detect

ROOT = Path(__file__).parent.parent
PPM = 200  # top-down raster resolution, pixels per meter (5 mm)
MARGIN_M = 0.3  # raster extends this far beyond the anchors

# Calibration knob: HSV ranges (OpenCV H is 0..179). Tune on real paint under real lighting.
# APWA color code -> (utility_class, [(h_lo, h_hi), ...])
COLORS = {
    "red": ("electric", [(0, 8), (172, 179)]),
    "orange": ("communications", [(9, 20)]),
    "yellow": ("gas", [(21, 35)]),
    "green": ("sewer", [(40, 85)]),
    "blue": ("water", [(95, 130)]),
    "purple": ("reclaimed_water", [(131, 160)]),
}
MIN_SAT, MIN_VAL = 110, 80
MIN_AREA_M2 = 0.003  # ignore blobs smaller than ~ 4 cm x 8 cm
GAP_M = 0.08  # paint gaps up to this size are bridged (dash gaps, another line painted across)
CELL_M = 0.03  # paint pixels are pooled into cells this size before tracing
MAX_NODES = 1500


class ScanError(Exception):
    pass


def site_raster(img: np.ndarray, anchors: dict[str, tuple[float, float]]):
    """Warp camera image to a metric top-down view. Returns (raster, raster_px -> site_xy function)."""
    found = {f"A{i + 1}": c.mean(axis=0) for i, c in detect(img).items()}
    ids = [a for a in anchors if a in found]
    if len(ids) < 4:
        raise ScanError(f"need 4 anchors in view, saw {sorted(found)}. Re-aim camera and rescan.")
    site = np.array([anchors[a] for a in ids], np.float64)
    h, _ = cv2.findHomography(np.array([found[a] for a in ids], np.float64), site)

    all_xy = np.array(list(anchors.values()))
    x0, y0 = all_xy.min(axis=0) - MARGIN_M
    x1, y1 = all_xy.max(axis=0) + MARGIN_M
    # site (x right, y up) -> raster (col right, row down)
    to_raster = np.array([[PPM, 0, -x0 * PPM], [0, -PPM, y1 * PPM], [0, 0, 1]])
    size = (round((x1 - x0) * PPM), round((y1 - y0) * PPM))
    raster = cv2.warpPerspective(img, to_raster @ h, size)
    return raster, lambda p: np.column_stack([x0 + p[:, 0] / PPM, y1 - p[:, 1] / PPM])


def _dijkstra(cost: np.ndarray, src: int):
    """Dense Dijkstra. Fine for the few hundred nodes a paint stroke produces."""
    n = len(cost)
    dist, prev, done = np.full(n, np.inf), np.full(n, -1), np.zeros(n, bool)
    dist[src] = 0
    for _ in range(n):
        u = int(np.argmin(np.where(done, np.inf, dist)))
        if not np.isfinite(dist[u]) or done[u]:
            break
        done[u] = True
        better = dist[u] + cost[u] < dist
        dist[better], prev[better] = dist[u] + cost[u][better], u
    return dist, prev


def centerline(mask: np.ndarray) -> np.ndarray:
    """Paint stroke -> ordered centerline points (raster px). Follows the paint itself, so bends,
    L and U shapes, and dashes all work: paint pixels are pooled into small cells, cells are linked
    to neighbours (across gaps up to GAP_M), and the line is the path between the two cells
    farthest apart along the paint.
    ponytail: a branching mark (T or Y) keeps only its longest run; split branches if real marks need it."""
    ys, xs = np.nonzero(mask)
    cell = max(2, round(CELL_M * PPM))
    _, inv = np.unique(np.column_stack([xs // cell, ys // cell]), axis=0, return_inverse=True)
    inv = inv.ravel()
    count = np.bincount(inv)
    nodes = np.column_stack([np.bincount(inv, xs) / count, np.bincount(inv, ys) / count])
    if len(nodes) > MAX_NODES:  # a huge blob is not a paint line; do not burn time on it
        nodes = nodes[:: len(nodes) // MAX_NODES + 1]
    d = np.linalg.norm(nodes[:, None] - nodes[None], axis=2)
    linked = d <= (1.5 * CELL_M + GAP_M) * PPM
    length = np.where(linked, d, np.inf)
    from_any = _dijkstra(length, 0)[0]
    start = int(np.argmax(np.where(np.isfinite(from_any), from_any, -1)))
    from_start = _dijkstra(length, start)[0]
    end = int(np.argmax(np.where(np.isfinite(from_start), from_start, -1)))
    # Squared hop cost: many short hops beat one long one, so the path hugs the paint through bends.
    _, prev = _dijkstra(np.where(linked, d ** 2, np.inf), start)
    path = [end]
    while path[-1] != start:
        path.append(int(prev[path[-1]]))
    line = nodes[path[::-1]]
    return cv2.approxPolyDP(line.astype(np.float32).reshape(-1, 1, 2), 0.02 * PPM, False).reshape(-1, 2)


def scan(img: np.ndarray, anchors: dict[str, tuple[float, float]]):
    """Returns (utilities in map-schema form, annotated top-down preview)."""
    raster, to_site = site_raster(img, anchors)
    hsv = cv2.cvtColor(raster, cv2.COLOR_BGR2HSV)
    strong = (hsv[..., 1] >= MIN_SAT) & (hsv[..., 2] >= MIN_VAL)
    k = round(GAP_M * PPM) | 1
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k))

    utilities, preview = [], raster.copy()
    for color, (utility_class, hues) in COLORS.items():
        hit = np.zeros(strong.shape, bool)
        for lo, hi in hues:
            hit |= (hsv[..., 0] >= lo) & (hsv[..., 0] <= hi)
        paint = hit & strong
        # Dilation only decides which strokes belong together (dashes, a line painted across).
        # Geometry comes from the real paint pixels, so bridging cannot shift the centerline.
        n, labels = cv2.connectedComponents(cv2.dilate(paint.astype(np.uint8), kernel))
        for i in range(1, n):
            stroke = (labels == i) & paint
            if stroke.sum() < MIN_AREA_M2 * PPM * PPM:
                continue
            line = centerline(stroke)
            cv2.polylines(preview, [line.astype(np.int32)], False, (255, 255, 255), 5)
            cv2.polylines(preview, [line.astype(np.int32)], False, (0, 0, 0), 2)
            cv2.putText(preview, f"U-{len(utilities) + 1:03d} {color}", tuple(line[0].astype(int) + (0, -8)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            utilities.append({
                "utility_id": f"U-{len(utilities) + 1:03d}",
                "utility_class": utility_class,
                "marking_color": color,
                "surface_marking": {
                    "centerline_m": [[round(float(x), 3), round(float(y), 3), 0.0] for x, y in to_site(line)],
                    "source_type": "overhead_camera",
                    "operator_reviewed": False,
                },
                "uploaded_layout": None,
                "depth_m": None,  # a camera cannot see depth. Stays unknown.
                "depth_status": "unknown",
                "evidence_relationship": "unregistered",
                "excavation_clearance_authorized": False,
            })
    return utilities, preview


def main():
    ap = argparse.ArgumentParser()
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--image")
    src.add_argument("--camera", type=int)
    ap.add_argument("--map", default=str(ROOT / "sample_data" / "map.json"), help="source of anchor positions")
    args = ap.parse_args()

    if args.image:
        img = cv2.imread(args.image)
    else:
        cam = cv2.VideoCapture(args.camera)
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        for _ in range(10):  # let auto-exposure settle
            ok, img = cam.read()
        cam.release()
        if ok:
            cv2.imwrite(str(ROOT / "sample_data" / "scan_source.jpg"), img)  # spec: keep source image
    if img is None:
        raise SystemExit("could not read image")

    anchors = {a["id"]: tuple(a["position_m"][:2]) for a in json.loads(Path(args.map).read_text())["anchors"]}
    try:
        utilities, preview = scan(img, anchors)
    except ScanError as e:
        raise SystemExit(f"scan rejected: {e}")
    cv2.imwrite(str(ROOT / "sample_data" / "scan_preview.jpg"), preview)
    (ROOT / "sample_data" / "scan.json").write_text(json.dumps(utilities, indent=2))
    print(f"{len(utilities)} candidate markings -> sample_data/scan.json, preview -> sample_data/scan_preview.jpg")
    for u in utilities:
        print(" ", u["utility_id"], u["marking_color"], u["surface_marking"]["centerline_m"])


if __name__ == "__main__":
    main()
