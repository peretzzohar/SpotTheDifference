const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8001";

async function request(path, options) {
  let response;
  try {
    response = await fetch(`${API_BASE_URL}${path}`, options);
  } catch (_error) {
    throw new Error("The backend is unavailable. Start the API and try again.");
  }
  const body = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(body.detail || "The request could not be completed.");
  return body;
}

export function compareImages(image1, image2) {
  const form = new FormData();
  form.append("image1", image1);
  form.append("image2", image2);
  return request("/api/compare", { method: "POST", body: form });
}

export function getDatasetSample(index = 0) {
  return request(`/api/dataset/sample?index=${encodeURIComponent(index)}`);
}

export { API_BASE_URL };
