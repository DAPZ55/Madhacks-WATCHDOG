"""Shared ArUco config. Edge (cv2) and phone (js-aruco2) must use the same dictionary."""
import cv2
import numpy as np

DICT_NAME = "ARUCO_MIP_36h12"  # same name in js-aruco2
DICT = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_ARUCO_MIP_36h12)


def tag_image(tag_id: int, px: int = 800) -> np.ndarray:
    """Tag with white quiet zone (detectors need it)."""
    return cv2.copyMakeBorder(
        cv2.aruco.generateImageMarker(DICT, tag_id, px),
        px // 6, px // 6, px // 6, px // 6, cv2.BORDER_CONSTANT, value=255,
    )


def detect(img: np.ndarray) -> dict[int, np.ndarray]:
    """Returns {tag_id: 4x2 corner pixels}."""
    corners, ids, _ = cv2.aruco.ArucoDetector(DICT).detectMarkers(img)
    return {} if ids is None else {int(i): c.reshape(4, 2) for i, c in zip(ids.flatten(), corners)}


# Calibration knob: focal length in pixels at 1920 px image width.
# 1990 = Logitech Brio 105 (58 degree diagonal field of view, from its spec sheet; not measured).
# Other cameras: f = 960 / tan(horizontal_fov / 2). C920-family (70 degrees) is 1360.
# With a near-overhead camera a wrong value barely affects distances: it scales depth, and
# lateral distance = pixel offset * depth / focal cancels it. It does shift the drawn pipe depth.
FOCAL_PX_AT_1920 = 1990.0


def survey(img: np.ndarray, size_m: float, tags: dict[int, np.ndarray] | None = None) -> dict[str, tuple[float, float]]:
    """Measure anchor centers from one image. Returns site-frame meters: A1 at origin, +X toward A2,
    +Y to the left of +X seen from above. Needs A1 and A2 in view; tags flat on one plane.
    Method: each tag's 3D position from its known size (solvePnP), then project onto the ground plane.
    ponytail: no lens undistortion, expect ~1-3% error. Tape-measure one distance to confirm."""
    tags = detect(img) if tags is None else tags
    if 0 not in tags or 1 not in tags:
        raise ValueError(f"need A1 and A2 in view, saw {sorted(f'A{i + 1}' for i in tags)}")
    ids = sorted(tags)
    h, w = img.shape[:2]
    f = FOCAL_PX_AT_1920 * w / 1920
    k = np.float64([[f, 0, w / 2], [0, f, h / 2], [0, 0, 1]])
    s = size_m / 2
    square = np.float64([[-s, s, 0], [s, s, 0], [s, -s, 0], [-s, -s, 0]])  # TL, TR, BR, BL
    pts = np.float64([
        cv2.solvePnP(square, tags[i].astype(np.float64), k, None, flags=cv2.SOLVEPNP_IPPE_SQUARE)[2].ravel()
        for i in ids
    ])
    origin = pts[ids.index(0)]
    x = pts[ids.index(1)] - origin
    x /= np.linalg.norm(x)
    # Ground normal: plane fit when 3+ tags, else "toward the camera". Camera sits at (0,0,0).
    n = np.linalg.svd(pts - pts.mean(axis=0))[2][-1] if len(ids) >= 3 else -pts.mean(axis=0)
    n = n - (n @ x) * x
    n /= np.linalg.norm(n)
    if n @ pts.mean(axis=0) > 0:
        n = -n
    y = np.cross(n, x)
    return {f"A{i + 1}": (round(float((q - origin) @ x), 3), round(float((q - origin) @ y), 3)) for i, q in zip(ids, pts)}
