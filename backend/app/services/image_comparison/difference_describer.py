import os
import logging

import numpy as np
from PIL import Image

from .difference_visualizer import as_data_url

DEFAULT_MODEL = "deepseek-ai/DeepSeek-V4-Flash-Vision-Exp"
logger = logging.getLogger(__name__)


class DifferenceDescriber:
    """Turn the pixel mask and source images into a readable change description."""

    def __init__(self) -> None:
        self.model = os.getenv("VISION_LANGUAGE_MODEL", DEFAULT_MODEL)
        self.token = os.getenv("HF_TOKEN") or self._logged_in_token()
        self._client = None
        self._reference_examples: list[str] | None = None

    @staticmethod
    def _logged_in_token() -> str | None:
        try:
            from huggingface_hub import get_token

            return get_token()
        except Exception:
            return None

    def describe(
        self,
        image1: Image.Image,
        image2: Image.Image,
        difference_image: Image.Image,
        mask: np.ndarray,
        bounding_box: list[int] | None,
    ) -> str:
        if not mask.any():
            return "No visible differences were detected between Image 1 and Image 2."

        generated = self._describe_with_vision_language_model(
            image1, image2, difference_image, bounding_box
        )
        if generated and not self._is_generic(generated):
            return generated
        return self._describe_from_mask(image1, image2, mask, bounding_box)

    @staticmethod
    def _is_generic(text: str) -> bool:
        normalized = text.lower()
        generic_phrases = (
            "visual change was detected",
            "a visual change was detected",
            "something changed",
            "there are differences",
            "red pixels",
            "changed area",
            "highlighted region",
        )
        return any(phrase in normalized for phrase in generic_phrases)

    def _describe_with_vision_language_model(
        self,
        image1: Image.Image,
        image2: Image.Image,
        difference_image: Image.Image,
        bounding_box: list[int] | None,
    ) -> str | None:
        if not self.token:
            return None
        try:
            from huggingface_hub import InferenceClient

            if self._client is None:
                self._client = InferenceClient(token=self.token)
            reference_examples = self._load_reference_examples()
            ai_images = [
                self._resize_for_analysis(image1),
                self._resize_for_analysis(image2),
                self._resize_for_analysis(difference_image),
            ]
            color_hint = self._source_color_hint(image1, image2, bounding_box)
            prompt = (
                "Compare the first image (Image 1) with the second image (Image 2). "
                "The third image is the Differences image and its red pixels are only an "
                "annotation mask, not an object or a color in the scene. Use that mask to "
                "focus your inspection, then identify the actual object or scene change by "
                "comparing the first two images. Determine colors and objects only from "
                "Image 1 and Image 2. Return one or more concise English sentences "
                "describing the change, never the red pixels or image layout. "
                "State whether an object was added, removed, changed, or moved, and mention "
                "its position or color when visible. Never answer only that there is a "
                f"difference. Source-color hint from the original images: {color_hint}.\n"
                f"Reference wording examples from the spot-the-diff dataset: {reference_examples}"
            )
            response = self._client.chat_completion(
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {"type": "image_url", "image_url": {"url": as_data_url(ai_images[0])}},
                            {"type": "image_url", "image_url": {"url": as_data_url(ai_images[1])}},
                            {"type": "image_url", "image_url": {"url": as_data_url(ai_images[2])}},
                        ],
                    }
                ],
                model=self.model,
                max_tokens=512,
            )
            text = response.choices[0].message.content
            if isinstance(text, list):
                text = " ".join(
                    item.get("text", "") if isinstance(item, dict) else str(item)
                    for item in text
                )
            if isinstance(text, str):
                text = text.strip().strip('"')
                return text if len(text.split()) >= 4 else None
        except Exception as error:
            logger.warning("Vision-language description unavailable: %s", error)
            return None
        return None

    @staticmethod
    def _resize_for_analysis(image: Image.Image, max_size: int = 768) -> Image.Image:
        resized = image.convert("RGB").copy()
        resized.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
        return resized

    def _load_reference_examples(self) -> str:
        if self._reference_examples is None:
            self._reference_examples = []
            try:
                from datasets import load_dataset

                dataset = load_dataset(
                    "Lancelot53/spot-the-diff", split="train", streaming=True
                )
                for sample in dataset:
                    sentences = sample.get("sentences") or []
                    self._reference_examples.extend(str(sentence) for sentence in sentences[:2])
                    if len(self._reference_examples) >= 4:
                        break
            except Exception:
                pass
        return " | ".join(self._reference_examples) or "No examples available."

    @staticmethod
    def _describe_from_mask(
        image1: Image.Image,
        image2: Image.Image,
        mask: np.ndarray,
        bounding_box: list[int] | None,
    ) -> str:
        height, width = mask.shape
        changed_pixels = mask.astype(bool)
        first_pixels = np.asarray(image1.convert("RGB"))[changed_pixels]
        second_pixels = np.asarray(image2.convert("RGB"))[changed_pixels]
        first_color = DifferenceDescriber._color_name(first_pixels.mean(axis=0))
        second_color = DifferenceDescriber._color_name(second_pixels.mean(axis=0))
        location = "the image"
        if bounding_box:
            center_x = (bounding_box[0] + bounding_box[2]) / 2 / width
            center_y = (bounding_box[1] + bounding_box[3]) / 2 / height
            horizontal = "left" if center_x < 0.34 else "right" if center_x > 0.66 else "center"
            vertical = "top" if center_y < 0.34 else "bottom" if center_y > 0.66 else "middle"
            location = (
                "the center of the image"
                if horizontal == "center" and vertical == "middle"
                else f"the {vertical} part of the image"
                if horizontal == "center"
                else f"the {horizontal} side of the image"
            )
        neutral_colors = {"white", "black", "gray"}
        if first_color in neutral_colors and second_color not in neutral_colors:
            return f"A {second_color}-colored visual element appeared on {location} in Image 2."
        if second_color in neutral_colors and first_color not in neutral_colors:
            return f"The {first_color}-colored visual element disappeared from {location} in Image 2."
        if first_color != second_color:
            return f"The visible color changed from {first_color} in Image 1 to {second_color} in Image 2 on {location}."
        return f"The visible content on {location} changed between Image 1 and Image 2; the specific object could not be identified confidently."

    @staticmethod
    def _source_color_hint(
        image1: Image.Image,
        image2: Image.Image,
        bounding_box: list[int] | None,
    ) -> str:
        if not bounding_box:
            return "unavailable"
        first = np.asarray(image1.convert("RGB"))
        second = np.asarray(image2.convert("RGB"))
        left, top, right, bottom = bounding_box
        first_mean = first[top:bottom + 1, left:right + 1].mean(axis=(0, 1))
        second_mean = second[top:bottom + 1, left:right + 1].mean(axis=(0, 1))
        return f"Image 1 is approximately {DifferenceDescriber._color_name(first_mean)}; Image 2 is approximately {DifferenceDescriber._color_name(second_mean)}"

    @staticmethod
    def _color_name(rgb: np.ndarray) -> str:
        red, green, blue = rgb
        if max(rgb) - min(rgb) < 24:
            return "white" if red > 220 else "black" if red < 40 else "gray"
        if red > green * 1.35 and red > blue * 1.35:
            return "red"
        if green > red * 1.25 and green > blue * 1.15:
            return "green"
        if blue > red * 1.25 and blue > green * 1.15:
            return "blue"
        if red > 160 and green > 120 and blue < 100:
            return "yellow"
        return "a mixed color"
