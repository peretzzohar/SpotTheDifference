require("dotenv").config();

const express = require("express");
const cors = require("cors");
const multer = require("multer");
const Redis = require("ioredis");
const { createDatabase, initializeDatabase } = require("./db");

const app = express();
const port = Number(process.env.PORT || 8001);
const redis = new Redis(process.env.REDIS_URL || "redis://localhost:6379", { lazyConnect: true, maxRetriesPerRequest: 1 });
const database = initializeDatabase(createDatabase(process.env.DATABASE_PATH || ":memory:"));
const upload = multer({ storage: multer.memoryStorage(), limits: { fileSize: Number(process.env.MAX_FILE_SIZE_BYTES || 10485760) } });
const inferenceApiUrl = process.env.INFERENCE_API_URL || "http://localhost:8009";

app.use(cors({ origin: (process.env.CORS_ORIGINS || "http://localhost:5172").split(",") }));
app.use(express.json());

app.get("/health", (_request, response) => response.json({ status: "ok", service: "backend" }));
app.post("/api/compare", upload.fields([{ name: "image1", maxCount: 1 }, { name: "image2", maxCount: 1 }]), async (request, response) => {
  const image1 = request.files?.image1?.[0];
  const image2 = request.files?.image2?.[0];
  if (!image1 || !image2) return response.status(400).json({ detail: "Both image1 and image2 are required." });
  try {
    const form = new FormData();
    form.append("image1", new Blob([image1.buffer], { type: image1.mimetype }), image1.originalname);
    form.append("image2", new Blob([image2.buffer], { type: image2.mimetype }), image2.originalname);
    const upstream = await fetch(`${inferenceApiUrl}/api/compare`, { method: "POST", body: form });
    const body = await upstream.json();
    return response.status(upstream.status).json(body);
  } catch (_error) {
    return response.status(503).json({ detail: "The comparison service is unavailable." });
  }
});
app.get("/api/dataset/sample", async (request, response) => {
  try {
    const index = Number(request.query.index || 0);
    const upstream = await fetch(`${inferenceApiUrl}/api/dataset/sample?index=${index}`);
    return response.status(upstream.status).json(await upstream.json());
  } catch (_error) {
    return response.status(503).json({ detail: "The dataset service is unavailable." });
  }
});

app.listen(port, () => console.log(`Backend listening on port ${port}`));

process.on("SIGTERM", () => { database.close(); redis.disconnect(); });
