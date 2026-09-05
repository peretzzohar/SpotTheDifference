import { useEffect, useState } from "react";

const MAX_FILE_SIZE = 10 * 1024 * 1024;
const ACCEPTED_TYPES = ["image/jpeg", "image/png", "image/webp"];

function ImageCard({ label, file, onChange }) {
  const [preview, setPreview] = useState("");
  useEffect(() => {
    if (!file) return setPreview("");
    const url = URL.createObjectURL(file);
    setPreview(url);
    return () => URL.revokeObjectURL(url);
  }, [file]);
  return <label className="upload-card"><span className="eyebrow">{label}</span><span className="upload-preview">{preview ? <img src={preview} alt={`${label} preview`} /> : <span className="upload-placeholder"><strong>+</strong><span>Choose an image</span><small>JPG, PNG, or WEBP</small></span>}</span><input type="file" accept=".jpg,.jpeg,.png,.webp" onChange={(event) => onChange(event.target.files?.[0] || null)} />{file && <span className="file-name">{file.name}</span>}</label>;
}

export default function ImageUploadForm({ onCompare, busy }) {
  const [image1, setImage1] = useState(null);
  const [image2, setImage2] = useState(null);
  const [error, setError] = useState("");
  function choose(setImage, file) {
    setError("");
    if (file && !ACCEPTED_TYPES.includes(file.type)) return setError("Use a JPG, PNG, or WEBP image.");
    if (file && file.size > MAX_FILE_SIZE) return setError("Each image must be smaller than 10 MB.");
    setImage(file);
  }
  function submit(event) {
    event.preventDefault();
    if (!image1 || !image2) return setError("Choose both images before comparing.");
    onCompare(image1, image2);
  }
  return <form className="compare-form" onSubmit={submit}><div className="upload-grid"><ImageCard label="Image 1" file={image1} onChange={(file) => choose(setImage1, file)} /><div className="swap-mark" aria-hidden="true">↔</div><ImageCard label="Image 2" file={image2} onChange={(file) => choose(setImage2, file)} /></div>{error && <p className="error-message" role="alert">{error}</p>}<button className="primary-button compare-button" type="submit" disabled={busy}>{busy ? "Analyzing images..." : "Compare images"}<span aria-hidden="true">→</span></button></form>;
}
