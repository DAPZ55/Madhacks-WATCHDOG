"""Draw 811 marking SYMBOLS (not just lines) the way locators paint them: arrows and owner initials,
corridor I-beams, oversized-utility bars with a size, conduit diamonds, termination E, offset arrows
with a distance, splice/valve circle-X, and NO/owner statements. Used by make_street_scenes.py.

Everything is in image pixels. Each draw_* returns the ground-truth record for that mark, with pixel
points still to be converted to site meters by the caller.
"""
import cv2
import numpy as np

STROKE = 14  # paint width, px
FONT = cv2.FONT_HERSHEY_SIMPLEX


def _frame(a, b):
    """Unit direction a->b and its left-hand perpendicular."""
    a, b = np.float64(a), np.float64(b)
    d = (b - a) / np.linalg.norm(b - a)
    return a, b, d, np.array([-d[1], d[0]])


def _line(img, p, q, color):
    cv2.line(img, tuple(np.int32(np.round(p))), tuple(np.int32(np.round(q))), color, STROKE, cv2.LINE_AA)


def _text(img, s, center, d, color, scale=1.5):
    """Paint text centered at `center`, running along direction d, never upside down."""
    if d[0] < 0:
        d = -d
    (w, h), _ = cv2.getTextSize(s, FONT, scale, 5)
    side = int(np.hypot(w, h)) + 20
    mask = np.zeros((side, side), np.uint8)
    cv2.putText(mask, s, ((side - w) // 2, (side + h) // 2), FONT, scale, 255, 5, cv2.LINE_AA)
    angle = np.degrees(np.arctan2(-d[1], d[0]))  # image y points down
    mask = cv2.warpAffine(mask, cv2.getRotationMatrix2D((side / 2, side / 2), angle, 1), (side, side))
    x0, y0 = int(center[0] - side / 2), int(center[1] - side / 2)
    xa, ya, xb, yb = max(x0, 0), max(y0, 0), min(x0 + side, img.shape[1]), min(y0 + side, img.shape[0])
    if xa < xb and ya < yb:
        region = mask[ya - y0:yb - y0, xa - x0:xb - x0] > 100
        img[ya:yb, xa:xb][region] = color
    return w


def _arrow(img, tip, d, color, size=46):
    """Arrowhead whose point is at `tip`, pointing along d."""
    perp = np.array([-d[1], d[0]])
    for side in (1, -1):
        _line(img, tip, tip - d * size + perp * side * size * 0.6, color)


def _gapped(img, a, b, d, color, gap_center, gap_half):
    """Stroke a->b leaving a hole for text or a symbol."""
    _line(img, a, gap_center - d * gap_half, color)
    _line(img, gap_center + d * gap_half, b, color)


def draw_line(img, pts, color, text):
    """<-- SBC -->  Path with arrows at both ends and the owner's initials in a gap."""
    pts = [np.float64(p) for p in pts]
    longest = max(range(len(pts) - 1), key=lambda i: np.linalg.norm(pts[i + 1] - pts[i]))
    for i in range(len(pts) - 1):
        a, b, d, _ = _frame(pts[i], pts[i + 1])
        if i == longest:
            mid = (a + b) / 2
            half = cv2.getTextSize(text, FONT, 1.5, 5)[0][0] / 2 + 30
            _gapped(img, a, b, d, color, mid, half)
            _text(img, text, mid, d, color)
        else:
            _line(img, a, b, color)
    _arrow(img, pts[0], _frame(pts[1], pts[0])[2], color)
    _arrow(img, pts[-1], _frame(pts[-2], pts[-1])[2], color)
    return {"type": "line", "points_px": pts}


def _glyph_pair(img, a, b, color, text, glyph):
    """Two identical glyphs near the ends of a->b with text between them (corridor, oversized, conduit)."""
    a, b, d, perp = _frame(a, b)
    length = np.linalg.norm(b - a)
    for c in (a + d * length * 0.14, b - d * length * 0.14):
        glyph(c, d, perp)
    _text(img, text, (a + b) / 2, d, color)
    return a, b


def draw_corridor(img, a, b, color, text):
    """|=| SRP |=|  I-beams: several lines in a corridor, count unknown."""
    def ibeam(c, d, perp):
        for s in (1, -1):
            _line(img, c + perp * s * 48 - d * 60, c + perp * s * 48 + d * 60, color)
        _line(img, c - perp * 48, c + perp * 48, color)
    a, b = _glyph_pair(img, a, b, color, text, ibeam)
    return {"type": "corridor", "points_px": [a, b]}


def draw_oversized(img, a, b, color, text):
    """=+= W 42" =+=  Large-diameter structure, size painted."""
    def bars(c, d, perp):
        _line(img, c - d * 85, c + d * 85, color)
        for s in (1, -1):
            _line(img, c + perp * s * 34 - d * 50, c + perp * s * 34 + d * 50, color)
        _line(img, c - perp * 62, c + perp * 62, color)
    a, b = _glyph_pair(img, a, b, color, text, bars)
    return {"type": "oversized", "points_px": [a, b]}


def draw_conduit(img, a, b, color, text):
    """=<>= USW DUCT =<>=  Duct or conduit: diamond between two bars."""
    def diamond(c, d, perp):
        for s in (1, -1):
            _line(img, c + perp * s * 50 - d * 62, c + perp * s * 50 + d * 62, color)
        corners = [c + d * 36, c + perp * 36, c - d * 36, c - perp * 36]
        for p, q in zip(corners, corners[1:] + corners[:1]):
            _line(img, p, q, color)
    a, b = _glyph_pair(img, a, b, color, text, diamond)
    return {"type": "conduit", "points_px": [a, b]}


def draw_termination(img, end, toward, color, text):
    """E-- MF 4" IHP  Dead end or stub-out at `end`; the facility runs toward `toward`."""
    end, toward, d, perp = _frame(end, toward)
    _line(img, end - perp * 48, end + perp * 48, color)
    for s in (1, -1):
        _line(img, end + perp * s * 48, end + perp * s * 48 + d * 42, color)
    _line(img, end, end + d * 120, color)
    w = cv2.getTextSize(text, FONT, 1.5, 5)[0][0]
    _text(img, text, end + d * (160 + w / 2), d, color)
    return {"type": "termination", "points_px": [end]}


def draw_offset(img, at, tip, color, owner, distance):
    """SBC ^ 12'  The facility is NOT under this mark: it lies `distance` away, the way the arrow points."""
    at, tip, d, perp = _frame(at, tip)
    _line(img, at, tip, color)
    _arrow(img, tip, d, color)
    _line(img, tip - perp * 62, tip + perp * 62, color)
    mid = (at + tip) / 2
    for s, label in ((-1, owner), (1, distance)):
        w = cv2.getTextSize(label, FONT, 1.5, 5)[0][0]
        _text(img, label, mid + perp * s * (w / 2 + 45), perp, color)
    return {"type": "offset", "points_px": [at, tip]}


def draw_splice(img, a, b, color, where=0.5):
    """-- (X) --  Buried splice, valve, or manhole on a line."""
    a, b, d, perp = _frame(a, b)
    c = a + (b - a) * where
    _gapped(img, a, b, d, color, c, 62)
    cv2.circle(img, tuple(np.int32(c)), 34, color, STROKE - 4, cv2.LINE_AA)
    for s in (1, -1):
        _line(img, c - (d + perp * s) * 20, c + (d + perp * s) * 20, color)
    return {"type": "splice", "points_px": [a, b, c]}


def draw_no_conflict(img, at, color, owner):
    """NO/MCI  That owner states it has no facilities in the requested area. Not an all-clear."""
    _text(img, f"NO/{owner}", np.float64(at), np.array([1.0, 0.0]), color, scale=1.7)
    return {"type": "no_conflict", "points_px": [np.float64(at)]}
