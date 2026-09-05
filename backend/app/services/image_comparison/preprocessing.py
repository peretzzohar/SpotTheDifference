from io import BytesIO

from PIL import Image, UnidentifiedImageError

SUPPORTED_FORMATS = {"JPEG", "PNG", "WEBP"}


def load_image(data: bytes, filename: str | None = None) -> Image.Image:
    if not data:
        raise ValueError("The uploaded image is empty.")
    try:
        with Image.open(BytesIO(data)) as image:
            image_format = (image.format or "").upper()
            if image_format not in SUPPORTED_FORMATS:
                raise ValueError("Use a JPG, JPEG, PNG, or WEBP image.")
            return image.convert("RGB").copy()
    except UnidentifiedImageError as error:
        raise ValueError("The uploaded file is not a valid image.") from error


def align_images(image1: Image.Image, image2: Image.Image) -> tuple[Image.Image, Image.Image]:
    width = max(image1.width, image2.width)
    height = max(image1.height, image2.height)
    return (
        image1.resize((width, height), Image.Resampling.LANCZOS),
        image2.resize((width, height), Image.Resampling.LANCZOS),
    )
