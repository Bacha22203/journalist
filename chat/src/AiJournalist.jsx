import React, { useState } from "react";
import "./styles.css"; // Import the custom CSS

const AiJournalist = () => {
  const [prompt, setPrompt] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);
  const [copied, setCopied] = useState(false);

  const handleSubmit = async () => {
    setLoading(true);
    try {
      const res = await fetch("http://127.0.0.1:8000/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt }),
      });

      if (!res.ok) throw new Error("Failed to generate content.");

      const data = await res.json();
      setResponse(data.generated_text || "No response received.");
    } catch (error) {
      setResponse(`Error: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  // Custom copy-to-clipboard function
  const handleCopy = () => {
    navigator.clipboard.writeText(response);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000); // Reset "Copied!" after 2 seconds
  };

  return (
    <div className="container fade-in">
      {/* Heading section */}
      <div className="heading-wrapper">
        <span className="icon">📰</span>
        <h2 className="heading">AI Journalist</h2>
      </div>

      {/* Textarea */}
      <textarea
        className="textarea"
        placeholder="Enter your request here..."
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        rows={4}/>

      {/* Character count */}
      <p className="character-count">
        Characters: {prompt.length}
      </p>

      {/* Generate button */}
      <button className="button" onClick={handleSubmit} disabled={loading}>
        {loading ? (
          <div className="spinner"></div>
        ) : (
          <>
            <span className="play-icon">▶</span>
            Generate
          </>
        )}
      </button>

      {/* Response section */}
      {response && (
        <div className="response visible">
          <div className="response-header">
            <h3>Generated Text:</h3>
            <button className="copy-button" onClick={handleCopy}>
              {copied ? "Copied!" : "Copy"}
            </button>
          </div>
          <p className="response-text">{response}</p>
        </div>
      )}
    </div>
  );
};

export default AiJournalist;
