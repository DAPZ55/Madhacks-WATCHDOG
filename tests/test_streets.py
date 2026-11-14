"""Check: every clean street scene scans back to its ground truth (same colors, line ends within
5 cm on the floor). Hard scenes are reported, not asserted: they contain road paint that color
detection is expected to mistake for utility marks (the AI validator's job).
Run: .venv/bin/python tests/test_streets.py"""
import json
import sys
from pathlib import Path

import cv2
import numpy as np

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
from edge.vision import scan

anchors = {a["id"]: tuple(a["position_m"][:2]) for a in json.loads((ROOT / "sample_data/map.json").read_text())["anchors"]}


def end_error(found, truth):
    """Worst distance from a truth line's two ends to the nearest end of the detected line."""
    ends = np.array([found[0][:2], found[-1][:2]])
    return max(np.min(np.linalg.norm(ends - np.array(t[:2]), axis=1)) for t in (truth[0], truth[-1]))


for image in sorted((ROOT / "sample_data/streets").glob("street_*.jpg")):
    truth = json.loads(image.with_suffix(".json").read_text())
    found, _ = scan(cv2.imread(str(image)), anchors)
    want = sorted(u["marking_color"] for u in truth["utilities"])
    got = sorted(u["marking_color"] for u in found)
    if truth["hard"]:
        extra = len(got) - len(want)
        print(f"{image.name} HARD: truth {want}, detected {got} -> {extra} false marking(s) from road paint")
        continue
    assert got == want, f"{image.name}: detected {got}, truth {want}"
    for t in truth["utilities"]:
        f = next(u for u in found if u["marking_color"] == t["marking_color"])
        err = end_error(f["surface_marking"]["centerline_m"], t["centerline_m"])
        assert err < 0.05, f"{image.name} {t['marking_color']}: line end off by {err:.3f} m"
    print(f"{image.name} ok: {got}")
