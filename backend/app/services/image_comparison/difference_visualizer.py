import base64
from io import BytesIO

from PIL import Image, ImageDraw


def as_data_url(image: Image.Image, image_format: str = "PNG") -> str:
    buffer = BytesIO()
    image.save(buffer, format=image_format)
    encoded = base64.b64encode(buffer.getvalue()).decode("ascii")
    return f"data:image/{image_format.lower()};base64,{encoded}"


def highlight_difference(
    image: Image.Image,
    mask,
    bounding_box: list[int] | None = None,
) -> Image.Image:
    result = image.convert("RGB").copy()
    pixels = result.load()
    for y in range(result.height):
        for x in range(result.width):
            if mask[y, x]:
                red, green, blue = pixels[x, y]
                pixels[x, y] = (255, min(green // 3, 90), min(blue // 3, 90))
    if bounding_box:
        draw = ImageDraw.Draw(result)
        draw.rectangle(tuple(bounding_box), outline=(255, 92, 55), width=max(3, result.width // 160))
    return result
