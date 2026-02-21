import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleAnalyze = async () => {
    if (!url.trim()) {
      alert("Enter a valid link");
      return;
    }

    setLoading(true);
    setResult(null);

    try {
      const response = await axios.post("http://127.0.0.1:8000/analyze", {
        url: url,
      });
      setResult(response.data);
    } catch (error) {
      alert("Error analyzing link");
      console.error(error);
    }

    setLoading(false);
  };

  return (
    <div className="container">
      <div className="card">
        <h1>Youtube Comments Analyzer</h1>

        <div className="input-group">
          <input
            type="text"
            placeholder="Paste YouTube link"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
          />

          <button onClick={handleAnalyze} disabled={loading}>
            {loading ? "Analyzing..." : "Analyze"}
          </button>
        </div>

        {loading && <div className="loader"></div>}

        {result && (
          <div className="results">
            <h2>Results</h2>

            <p><strong>Platform:</strong> {result.platform}</p>
            <p><strong>Total Comments:</strong> {result.total_comments}</p>

            <h3>Sentiment Breakdown</h3>

            <div className="bar positive">
              Positive: {result.sentiment_analysis.positive}%
            </div>

            <div className="bar negative">
              Negative: {result.sentiment_analysis.negative}%
            </div>

            <div className="bar neutral">
              Neutral: {result.sentiment_analysis.neutral}%
            </div>

            <h3>Summary</h3>
            <div className="summary-box">
              {result.summary}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;