import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const handleAnalyze = async () => {
    if (!url.trim()) {
      setError("Please enter a YouTube link.");
      return;
    }

    setLoading(true);
    setResult(null);
    setError("");

    try {
      const response = await axios.post("http://127.0.0.1:8000/analyze", {
        url: url,
      });
      setResult(response.data);
    } catch (err) {
      setError("Failed to analyze. Make sure the link is valid.");
    }

    setLoading(false);
  };

  return (
    <div className="container">
      <h1 className="title">YouTube Comments Analyzer</h1>

      <div className="input-section">
        <input
          type="text"
          placeholder="Paste YouTube link here..."
          value={url}
          onChange={(e) => setUrl(e.target.value)}
        />

        <button onClick={handleAnalyze} disabled={loading}>
          {loading ? "Analyzing..." : "Analyze"}
        </button>
      </div>

      {error && <div className="error">{error}</div>}

      {result && (
        <div className="result-card">
          <h2>Results</h2>

          <p><strong>Platform:</strong> {result.platform}</p>
          <p><strong>Total Comments:</strong> {result.total_comments}</p>

          <h3>Sentiment Breakdown</h3>

          <div className="sentiment positive">
            Positive: {result.sentiment_analysis.positive}%
          </div>

          <div className="sentiment negative">
            Negative: {result.sentiment_analysis.negative}%
          </div>

          <div className="sentiment neutral">
            Neutral: {result.sentiment_analysis.neutral}%
          </div>

          <h3>AI Summary</h3>
          <div className="summary-box">
            {result.summary}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
