FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/app ./backend/app
COPY inference ./inference
COPY ml ./ml
COPY models ./models
ENV PYTHONPATH=/app PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
EXPOSE 8009
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8009"]
