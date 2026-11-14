"""Write printable anchor tags A1..A4 (ids 0..3) to sample_data/tags/.
Print, then MEASURE the black square's side with a ruler: that is size_m in the map."""
import sys
from pathlib import Path

import cv2

sys.path.insert(0, str(Path(__file__).parent.parent))
from edge.tags import tag_image

out = Path(__file__).parent.parent / "sample_data" / "tags"
out.mkdir(parents=True, exist_ok=True)
for tag_id in range(4):
    img = tag_image(tag_id)
    cv2.putText(img, f"A{tag_id + 1} (id {tag_id})", (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.5, 0, 3)
    cv2.imwrite(str(out / f"A{tag_id + 1}.png"), img)
print("wrote", out)
