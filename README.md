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

## Activate the app with Docker

Prerequisites:

- Docker Desktop must be installed and running.
- Docker Compose must be available through `docker compose`.

From the project root (`D:\where's-waldo`), run:

```bash
docker compose up --build
```

The first run builds the frontend, backend, and inference images. Keep this terminal open while using the app. Open `http://localhost:5172` in a browser.

Docker service URLs:

- Frontend: `http://localhost:5172`
- Node gateway: `http://localhost:8001`
- FastAPI inference service: `http://localhost:8009`

To stop the app, press `Ctrl+C`. To stop and remove the containers and their Compose network, run:

```bash
docker compose down
```

To also remove the named application volumes, use `docker compose down -v`. The Redis and worker services preserve the original skeleton architecture for future asynchronous processing. The current comparison request is synchronous so the UI can show its result immediately.

## Activate the app locally

Prerequisites:

- Node.js 20 or newer and npm.
- Python 3.11 or newer.
- Redis running locally at `localhost:6379` if you want to use the worker architecture.

Run the following from the project root. Use separate terminals for each long-running service.

### 1. Configure Python

Copy the environment template and create a virtual environment:

```bash
copy .env.example .env
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

In Git Bash, the activation command is:

```bash
source .venv/Scripts/activate
```

### 2. Start the FastAPI comparison service

In a terminal with the virtual environment activated:

```bash
uvicorn backend.app.main:app --reload --port 8009
```

The inference API is available at `http://localhost:8009`.

### 3. Start the Node gateway

In a second terminal:

```bash
cd backend
npm install
npm run dev
```

The gateway is available at `http://localhost:8001`.

### 4. Start the React frontend

In a third terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the Vite URL shown in the terminal, normally `http://localhost:5172`. The frontend sends comparison requests to the Node gateway, which forwards them to FastAPI.

To stop a local service, press `Ctrl+C` in its terminal. If you only want to check the frontend without the backend, run `npm run build` from `frontend`; image comparison itself requires both backend services to be running.

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
