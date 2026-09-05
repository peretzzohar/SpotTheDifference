# Where's Waldo — Image Difference Detector

A modular image comparison application that accepts two images, identifies visual changes, highlights detected differences, and reports confidence and processing time.

The default comparator is a transparent pixel-based baseline designed to be replaced by an ML model in the future.

## Architecture

* `frontend`: React 18 + Vite interface with Comparison, Results, Dataset Demo, and About views.
* `backend`: Node.js + Express gateway running on port `8001`. It validates multipart requests and proxies comparison and dataset requests.
* `backend/app`: FastAPI inference service contract and comparison modules.
* `backend/app/services/image_comparison`: Image loading and alignment, pixel comparison, and difference visualization.
* `inference`: FastAPI Docker entry point and worker boundary.
* `ml`: Future training and evaluation module boundaries.
* `docker-compose.yml`: Redis, Node gateway, FastAPI inference, worker, and frontend services.

## Running the App with Docker

### Prerequisites

* Docker Desktop must be installed and running.
* Docker Compose must be available through `docker compose`.

From the project root:

```bash
docker compose up --build
```

The first run builds the frontend, backend, and inference images.

Keep the terminal open while using the application.

Open:

`http://localhost:5172`

### Docker Service URLs

| Service           | URL                     |
| ----------------- | ----------------------- |
| Frontend          | `http://localhost:5172` |
| Node Gateway      | `http://localhost:8001` |
| FastAPI Inference | `http://localhost:8009` |

### Stop the Application

Press `Ctrl+C` in the terminal running Docker Compose.

To stop and remove the containers and their Compose network:

```bash
docker compose down
```

To also remove the named application volumes:

```bash
docker compose down -v
```

The Redis and worker services preserve the original skeleton architecture for future asynchronous processing. The current image-comparison request is synchronous so the UI can display results immediately.

## Running the App Locally

### Prerequisites

* Node.js 20 or newer
* npm
* Python 3.11 or newer
* Redis running locally at `localhost:6379` if you want to use the worker architecture

Run the following commands from the project root in Git Bash.

Use separate terminals for each long-running service.

### 1. Configure Python

Copy the environment template:

```bash
cp .env.example .env
```

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/Scripts/activate
```

Install the Python dependencies:

```bash
python -m pip install -r requirements.txt
```

If the virtual environment already exists, activate it directly:

```bash
source .venv/Scripts/activate
```

#### Windows Command Prompt

If you are using Windows Command Prompt instead of Git Bash:

```cmd
copy .env.example .env
.venv\Scripts\activate
```

### 2. Start the FastAPI Comparison Service

In a terminal with the virtual environment activated:

```bash
uvicorn backend.app.main:app --reload --port 8009
```

The inference API will be available at:

`http://localhost:8009`

### 3. Start the Node Gateway

Open a second terminal:

```bash
cd backend
npm install
npm run dev
```

The gateway will be available at:

`http://localhost:8001`

### 4. Start the React Frontend

Open a third terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the Vite URL shown in the terminal, normally:

`http://localhost:5172`

The frontend sends comparison requests to the Node gateway, which forwards them to the FastAPI inference service.

To stop a local service, press `Ctrl+C` in its terminal.

If you only want to verify that the frontend builds correctly without running the backend:

```bash
cd frontend
npm run build
```

Image comparison itself requires both backend services to be running.

## API

### `GET /health`

Returns the gateway health status.

### `POST /api/compare`

Accepts a multipart request containing:

* `image1`
* `image2`

Supported image formats:

* JPG
* JPEG
* PNG
* WEBP

Maximum size:

* 10 MB per image

A successful comparison response contains:

* `success`
* `differences`
* `difference_image` — PNG data URL containing the visual difference result
* aligned image dimensions
* `processing_time`

Each detected difference includes:

* description
* confidence
* changed-area percentage
* bounding box when a change is detected

### `GET /api/dataset/sample?index=0`

Loads a single external Spot-the-Diff dataset sample on demand.

## Dataset Integration

The Dataset Demo uses the Hugging Face dataset:

`Lancelot53/spot-the-diff`

The dataset is accessed with:

```python
from datasets import load_dataset

ds = load_dataset("Lancelot53/spot-the-diff", split="train")
```

The dataset is loaded **only when a demo sample is requested**.

It is not:

* downloaded during project setup
* copied into the repository
* bundled into a Docker image
* placed in the frontend
* stored in a project `dataset/` directory

Dataset access requires network connectivity and the Python `datasets` package.

## Comparison and ML Extension

`ImageComparator.compare(image1, image2)` is the stable comparison boundary.

The current implementation:

1. Aligns the input images.
2. Measures pixel-level differences.
3. Removes small areas of noise.
4. Creates a red-highlight difference visualization.
5. Returns structured comparison findings.

The comparison layer is designed to support a future ML implementation.

A future model can implement the same interface or be injected behind the comparison service without requiring changes to the API or frontend contract.

**No ML model is trained when the application starts.**

## Safety and Storage

Uploads are held in memory for the duration of the comparison request.

This project does not commit or permanently store:

* user uploads
* generated images
* datasets
* databases
* credentials
* model weights
* caches
* logs
* environment files

`.gitignore` excludes these paths and artifact types.

`.env.example` contains placeholders and local service defaults only.
