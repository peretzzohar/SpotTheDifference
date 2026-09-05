from dataclasses import dataclass

import numpy as np
from PIL import Image, ImageChops, ImageEnhance, ImageFilter, ImageOps

from .difference_visualizer import as_data_url, highlight_difference
from .difference_describer import DifferenceDescriber
from .preprocessing import align_images


@dataclass
class ComparisonResult:
    differences: list[dict]
    difference_image: str
    image_width: int
    image_height: int


class ImageComparator:
    """Pixel-based baseline with a stable interface for a future ML comparator."""

    def __init__(self) -> None:
        self.describer = DifferenceDescriber()

    def compare(self, image1: Image.Image, image2: Image.Image) -> ComparisonResult:
        first, second = align_images(image1, image2)
        difference = ImageChops.difference(first, second)
        grayscale = ImageOps.grayscale(difference)
        enhanced = ImageEnhance.Contrast(grayscale).enhance(2.0)
        softened = enhanced.filter(ImageFilter.MedianFilter(size=3))
        pixels = np.asarray(softened, dtype=np.uint8)
        mask = pixels >= 32
        changed = int(mask.sum())
        total = mask.size
        coverage = changed / total if total else 0.0

        bounding_box = None
        if changed == 0:
            differences = [{"description": "No visible differences detected.", "confidence": 0.98}]
        else:
            ys, xs = np.where(mask)
            bounding_box = [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]
            differences = [{
                "description": "Visual changes detected in the highlighted region.",
                "confidence": round(min(0.99, 0.55 + coverage * 4), 2),
                "bounding_box": bounding_box,
                "changed_area_percent": round(coverage * 100, 2),
            }]

        visualization = highlight_difference(first, mask, bounding_box)
        description = self.describer.describe(first, second, visualization, mask, bounding_box)
        differences[0]["description"] = description
        return ComparisonResult(
            differences=differences,
            difference_image=as_data_url(visualization),
            image_width=first.width,
            image_height=first.height,
        )
