# -Where'sWaldo Image Difference Detector

A modular image comparison application that accepts two images, highlights visual changes, and reports confidence and processing time. The default comparator is a transparent pixel-based baseline designed to be replaced by an ML model later.

## Architecture

- `frontend`: React 18 + Vite interface with comparison, results, Dataset Demo, and About views.
- `backend`: Node.js + Express gateway on port 8001. It validates multipart requests and proxies comparison and dataset requests.
- `backend/app`: FastAPI inference service contract and comparison modules.
- `backend/app/services/image_comparison`: image loading/alignment, pixel comparison, and difference visualization.
- `inference`: FastAPI Docker entry point and worker boundary.
- `ml`: future training/evaluation module boundaries.
- `docker-compose.yml`: Redis, Node gateway, FastAPI inference, worker, and frontend services.

## Run with Docker

From the project root:

```bash
docker compose up --build
```

Open `http://localhost:5172`. The frontend uses the Node gateway at `http://localhost:8001`; the gateway calls the internal FastAPI service at `http://inference:8009`.

The Redis and worker services preserve the original skeleton architecture for future asynchronous processing. The current comparison request is synchronous so the UI can show its result immediately.

## Local development

1. Copy `.env.example` to `.env` and adjust local values if needed.
2. Install frontend dependencies and start Vite:

   ```bash
   cd frontend
   npm install
   npm run dev
   ```

3. Install Python dependencies from the project root:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Start the FastAPI service from the project root:

   ```bash
   uvicorn backend.app.main:app --reload --port 8009
   ```

5. Start the Node gateway in another terminal:

   ```bash
   cd backend
   npm install
   npm run dev
   ```

## API

- `GET /health`: gateway health response.
- `POST /api/compare`: multipart request with `image1` and `image2`. Supports JPG, JPEG, PNG, and WEBP up to 10 MB each.
- `GET /api/dataset/sample?index=0`: loads one external Spot-the-Diff sample on demand.

A comparison response contains `success`, `differences`, `difference_image` as a PNG data URL, aligned image dimensions, and `processing_time`. Each difference includes a description, confidence, changed-area percentage, and bounding box when a change is detected.

## Dataset integration

The Dataset Demo references the Hugging Face dataset `Lancelot53/spot-the-diff` through:

```python
from datasets import load_dataset

ds = load_dataset("Lancelot53/spot-the-diff", split="train")
```

The dataset is loaded only when a demo sample is requested. It is not downloaded during project setup, copied into the repository, bundled into a Docker image, placed in the frontend, or stored in a project `dataset/` directory. Dataset availability requires network access and the `datasets` package.

## Comparison and ML extension

`ImageComparator.compare(image1, image2)` is the stable comparison boundary. The current implementation aligns images, measures pixel differences, removes small noise, creates a red-highlight visualization, and returns structured findings. A future model can implement the same interface or be injected behind this service without changing the API or frontend contract. No model is trained when the application starts.

## Safety and storage

Uploads are held in memory for the comparison request. This template does not commit user uploads, generated images, datasets, databases, credentials, model weights, caches, logs, or environment files. `.gitignore` excludes those paths and artifact types. `.env.example` contains placeholders and local service defaults only.
