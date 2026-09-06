import { useEffect, useState } from "react";
import ImageUploadForm from "./components/ImageUploadForm";
import ImageAnalysisResult from "./components/ImageAnalysisResult";
import DatasetDemo from "./components/DatasetDemo";
import { compareImages } from "./services/api";

export default function App() {
  const [theme, setTheme] = useState(() => localStorage.getItem("theme") === "dark" ? "dark" : "light");
  const [result, setResult] = useState(null);
  const [view, setView] = useState("compare");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [sources, setSources] = useState({ image1: "", image2: "" });
  const [uploadVersion, setUploadVersion] = useState(0);
  useEffect(() => {
    const root = document.documentElement;
    if (theme === "system") root.removeAttribute("data-theme");
    else root.dataset.theme = theme;
    localStorage.setItem("theme", theme);
  }, [theme]);
  function toggleTheme() {
    setTheme((currentTheme) => currentTheme === "dark" ? "light" : "dark");
  }
  async function handleCompare(image1, image2) {
    setBusy(true); setError("");
    setSources({ image1: URL.createObjectURL(image1), image2: URL.createObjectURL(image2) });
    try { setResult(await compareImages(image1, image2)); } catch (requestError) { setError(requestError.message); } finally { setBusy(false); }
  }
  function reupload() {
    setResult(null);
    setError("");
    setSources({ image1: "", image2: "" });
    setUploadVersion((version) => version + 1);
    window.scrollTo({ top: 0, behavior: "smooth" });
  }
  return <><header className="site-header"><a className="brand" href="#compare" onClick={() => setView("compare")}><span className="brand-mark">W</span><span>-SpotTheDifference</span></a><nav><button className={view === "compare" ? "active" : ""} onClick={() => setView("compare")}>Compare</button><button className={view === "dataset" ? "active" : ""} onClick={() => setView("dataset")}>Dataset Demo</button><button className={view === "about" ? "active" : ""} onClick={() => setView("about")}>About</button><button className={`theme-toggle ${theme === "dark" ? "dark" : "light"}`} type="button" onClick={toggleTheme} aria-label={`Switch to ${theme === "dark" ? "light" : "dark"} mode`} aria-pressed={theme === "dark"}><span className="toggle-track"><span className="toggle-thumb" aria-hidden="true">{theme === "dark" ? <svg className="moon-icon" viewBox="0 0 24 24" focusable="false"><path d="M20.6 14.7A8.7 8.7 0 0 1 9.3 3.4a9 9 0 1 0 11.3 11.3z" /></svg> : <svg className="sun-icon" viewBox="0 0 24 24" focusable="false"><circle cx="12" cy="12" r="5" /><path d="M12 1.5v3M12 19.5v3M22.5 12h-3M4.5 12h-3M19.4 4.6l-2.2 2.2M6.8 17.2l-2.2 2.2M19.4 19.4l-2.2-2.2M6.8 6.8L4.6 4.6" /></svg>}</span></span></button></nav></header><main>{view === "compare" && <><section className="hero"><span className="eyebrow">Image intelligence</span><h1>Spot what changed.</h1><p>Compare two images side by side and get a clear visual map of every meaningful difference.</p></section><ImageUploadForm key={uploadVersion} onCompare={handleCompare} busy={busy} />{error && <p className="error-message page-error" role="alert">{error}</p>}{result && <ImageAnalysisResult result={result} image1={sources.image1} image2={sources.image2} onReupload={reupload} />}</>}{view === "dataset" && <><section className="hero compact"><span className="eyebrow">Developer tools / 02</span><h1>Explore the reference set.</h1><p>Inspect individual Spot-the-Diff samples without copying the dataset into the application.</p></section><DatasetDemo /></>}{view === "about" && <section className="about-section"><span className="eyebrow">About / 03</span><h1>A modular difference detector.</h1><p>The current comparator uses a transparent pixel-based baseline with alignment, noise reduction, and highlighted output. Its interface is deliberately isolated so a trained model can replace it later.</p><div className="about-grid"><article><span>01</span><h2>Private by default</h2><p>Uploaded images are processed in memory and are not persisted by the comparison service.</p></article><article><span>02</span><h2>External dataset</h2><p>The Lancelot53/spot-the-diff dataset is requested from Hugging Face only when the demo is used.</p></article><article><span>03</span><h2>Ready for ML</h2><p>The comparator contract can later route to a model trained or evaluated outside the request path.</p></article></div></section>}</main></>;
}
