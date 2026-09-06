import { useState } from "react";
import { getDatasetSample } from "../services/api";

export default function DatasetDemo() {
  const [sample, setSample] = useState(null);
  const [index, setIndex] = useState(0);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  async function loadSample() {
    setLoading(true); setError("");
    try { setSample(await getDatasetSample(index)); } catch (requestError) { setError(requestError.message); } finally { setLoading(false); }
  }
  return <section className="demo-section"><div className="section-heading"><div><span className="eyebrow">External reference</span><h2>Dataset Demo</h2></div><span className="dataset-tag">Lancelot53/spot-the-diff</span></div><p className="muted">Samples load on demand from Hugging Face and are never stored in this project.</p><div className="demo-controls"><label>Sample index <input type="number" min="0" value={index} onChange={(event) => setIndex(Math.max(0, Number(event.target.value) || 0))} /></label><button className="secondary-button" type="button" onClick={loadSample} disabled={loading}>{loading ? "Loading..." : "Load sample"}</button></div>{error && <p className="error-message" role="alert">{error}</p>}{sample && <div className="sample-result"><div className="sample-images"><img src={sample.image_a} alt="Dataset image A" /><img src={sample.image_b} alt="Dataset image B" /></div><p><strong>Expected difference</strong>{sample.expected_difference}</p></div>}</section>;
}
