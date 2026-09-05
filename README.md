Sure — here is the **super-short version**:

# SpotTheDifference

Full-stack image comparison app that detects and highlights differences between two images.

## Tech Stack

React · Node.js · Express · FastAPI · Python · Pillow · NumPy · Docker

## Run with Docker

```bash
docker compose up --build
```

Open: `http://localhost:5173`

Service endpoints:

* Frontend: `http://localhost:5173`
* Node.js backend: `http://localhost:8002`
* FastAPI health: `http://localhost:8010/health`
* Redis: `localhost:6380`

## Run Locally

```bash
python -m venv .venv
source .venv/Scripts/activate
python -m pip install -r requirements.txt
```

**FastAPI:**

```bash
python -m uvicorn backend.app.main:app --reload --port 8010
```

To enable natural-language change descriptions from the red-marked Differences image, set a Hugging Face access token before starting FastAPI:

```bash
export HF_TOKEN=your_huggingface_token
```

The service sends Image 1, Image 2, and the generated Differences image to the configured vision-language model. Without `HF_TOKEN`, it keeps the comparison service available and returns a mask-based description with the changed region.

**Backend:**

```bash
cd backend
npm install
npm run dev
```

The local backend listens on port `8002` and the local FastAPI service listens on port `8010`.

**Frontend:**

```bash
cd frontend
npm install
npm run dev
```

## Dataset

Uses the Hugging Face **Lancelot53/spot-the-diff** dataset, loaded on demand.

This is enough for a clean GitHub README without unnecessary documentation.
