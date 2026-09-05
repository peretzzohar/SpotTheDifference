Sure — here is the **super-short version**:

# SpotTheDifference

Full-stack image comparison app that detects and highlights differences between two images.

## Tech Stack

React · Node.js · Express · FastAPI · Python · Pillow · NumPy · Docker

## Run with Docker

```bash
docker compose up --build
```

Open: `http://localhost:5172`

## Run Locally

```bash
python -m venv .venv
source .venv/Scripts/activate
python -m pip install -r requirements.txt
```

**FastAPI:**

```bash
python -m uvicorn backend.app.main:app --reload --port 8009
```

**Backend:**

```bash
cd backend
npm install
npm run dev
```

**Frontend:**

```bash
cd frontend
npm install
npm run dev
```

## Dataset

Uses the Hugging Face **Lancelot53/spot-the-diff** dataset, loaded on demand.

This is enough for a clean GitHub README without unnecessary documentation.
