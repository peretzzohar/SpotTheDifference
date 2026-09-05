from io import BytesIO

from PIL import Image

DATASET_ID = "Lancelot53/spot-the-diff"


def _first_value(sample: dict, names: tuple[str, ...]):
    for name in names:
        if name in sample and sample[name] is not None:
            return sample[name]
    return None


def _image_data_url(value) -> str | None:
    if value is None:
        return None
    if isinstance(value, Image.Image):
        image = value.convert("RGB")
    elif isinstance(value, dict) and value.get("bytes"):
        image = Image.open(BytesIO(value["bytes"])).convert("RGB")
    else:
        return None
    output = BytesIO()
    image.save(output, format="JPEG", quality=82)
    import base64
    return "data:image/jpeg;base64," + base64.b64encode(output.getvalue()).decode("ascii")


def get_sample(index: int = 0) -> dict:
    """Load one external sample on demand; the dataset is never stored in this project."""
    from datasets import load_dataset

    dataset = load_dataset(DATASET_ID, split="train")
    if len(dataset) == 0:
        raise ValueError("The dataset contains no samples.")
    sample = dataset[index % len(dataset)]
    image_a = _first_value(sample, ("image1", "image_a", "image_1", "left", "image"))
    image_b = _first_value(sample, ("image2", "image_b", "image_2", "right", "image_changed"))
    description = _first_value(sample, ("difference", "differences", "description", "caption", "text", "sentences"))
    if isinstance(description, list):
        description = " ".join(str(sentence) for sentence in description)
    return {
        "dataset": DATASET_ID,
        "index": index % len(dataset),
        "image_a": _image_data_url(image_a),
        "image_b": _image_data_url(image_b),
        "expected_difference": str(description or "No description provided by this sample."),
    }
