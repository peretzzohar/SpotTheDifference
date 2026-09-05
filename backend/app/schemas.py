from pydantic import BaseModel

class Detection(BaseModel):
    class_name: str
    confidence: float
    bbox: list[float]
    color: str | None = None
    clothing: dict[str, str] | None = None
    description: str | None = None

class ImageAnalysisResponse(BaseModel):
    detections: list[Detection]
    image_width: int
    image_height: int
    description: str
