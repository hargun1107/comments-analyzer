import React, { useState } from "react";
import axios from "axios";

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
    <div style={{ padding: "40px", fontFamily: "Arial" }}>
      <h1>Comments Analyzer</h1>

      <input
        type="text"
        placeholder="Paste YouTube/Instagram/Twitter/Facebook link"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        style={{
          padding: "10px",
          width: "400px",
          borderRadius: "8px",
          border: "1px solid #aaa",
        }}
      />

      <button
        onClick={handleAnalyze}
        style={{
          padding: "10px 20px",
          marginLeft: "10px",
          borderRadius: "8px",
          background: "black",
          color: "white",
          border: "none",
        }}
      >
        Analyze
      </button>

      {loading && <p>Analyzing…</p>}

      {result && (
        <div style={{ marginTop: "30px" }}>
          <h2>Results</h2>

          <p><b>Platform:</b> {result.platform}</p>
          <p><b>Total Comments:</b> {result.total_comments}</p>

          <h3>Sentiment Breakdown</h3>
          <ul>
            <li>Positive: {result.sentiment_analysis.positive}</li>
            <li>Negative: {result.sentiment_analysis.negative}</li>
            <li>Neutral: {result.sentiment_analysis.neutral}</li>
          </ul>

          <h3>Summary</h3>
          <p>{result.summary}</p>
        </div>
      )}
    </div>
  );
}

export default App;
