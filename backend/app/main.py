from time import perf_counter

from fastapi import FastAPI, File, HTTPException, Query, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .services.dataset_service import get_sample
from .services.image_comparison.comparator import ImageComparator
from .services.image_comparison.preprocessing import load_image

app = FastAPI(title=settings.api_title, version=settings.api_version)
app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origins_list, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
comparator = ImageComparator()

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "inference"}

@app.post("/api/compare")
async def compare(image1: UploadFile = File(...), image2: UploadFile = File(...)) -> dict:
    started = perf_counter()
    try:
        first = load_image(await image1.read(), image1.filename)
        second = load_image(await image2.read(), image2.filename)
        result = comparator.compare(first, second)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    return {
        "success": True,
        "differences": result.differences,
        "difference_image": result.difference_image,
        "image_width": result.image_width,
        "image_height": result.image_height,
        "processing_time": round(perf_counter() - started, 4),
    }


@app.post("/api/v1/analyze")
async def analyze(image: UploadFile = File(...)) -> dict:
    raise HTTPException(status_code=410, detail="The single-image endpoint was replaced by /api/compare.")


@app.get("/api/dataset/sample")
def dataset_sample(index: int = Query(default=0, ge=0)) -> dict:
    try:
        return get_sample(index)
    except Exception as error:
        raise HTTPException(status_code=503, detail="The external dataset is unavailable right now.") from error
