import React, { useState } from "react";
import axios from "axios";
import "./App.css";




function UploadPage() {
  const [file, setFile] = useState(null);
  const [url, setUrl] = useState("");
  const [message, setMessage] = useState("");
  const [diagramUrl, setDiagramUrl] = useState("");
  const [email, setEmail] = useState("");


  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUrlChange = (e) => {
    setUrl(e.target.value);
  };

  const handleSubmitFile = async (e) => {
    e.preventDefault();
    if (!file) {
      setMessage("Please select a file to upload.");
      return;
    }
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post("http://127.0.0.1:5000/api/analyze-file", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      setMessage("Analysis completed!");
      setDiagramUrl("http://127.0.0.1:5000" + response.data.diagram_url);
    } catch (error) {
      console.error("Erreur lors de l'analyse du fichier :", error.response?.data || error);
      setMessage("Error analyzing the file.");
    }
  };

  const handleSendEmail = async () => {
    const email = prompt("Enter your email to receive the diagram:");
    if (!email || !diagramUrl) return;
  
    try {
      const response = await axios.post('http://127.0.0.1:5000/send-email', {
        email,
        diagram_url: diagramUrl
      });
  
      if (response.status === 200) {
        alert("✅ Email sent successfully!");
      } else {
        alert("❌ Failed to send email.");
      }
    } catch (error) {
      console.error("❌ Error sending email:", error);
      alert("❌ Error sending email.");
    }
  };
  

  const handleSubmitUrl = async (e) => {
    e.preventDefault();
    if (!url) {
      setMessage("Please enter a URL.");
      return;
    }

    try {
      const response = await axios.post("http://127.0.0.1:5000/api/analyze-url", { url });

      setMessage("Analysis completed!");
      setDiagramUrl("http://127.0.0.1:5000" + response.data.diagram_url);
    } catch (error) {
      console.error("Erreur lors de l'analyse de l'URL :", error.response?.data || error);
      setMessage("Error analyzing the URL.");
    }
  };

  return (
    <div className="App">
      <section className="upload-wrapper">
  <div className="upload-card">
    <h1 className="upload-title">Welcome to Kano Analyzer</h1>
    <p className="upload-subtitle">Start by uploading your file or entering a URL.</p>

    <form className="upload-form" onSubmit={handleSubmitFile}>
      <div className="input-group">
        <label>Upload a file:</label>
        <input type="file" accept=".pdf,.docx,.csv,.txt" onChange={handleFileChange} />
      </div>
      <button type="submit">Analyze File</button>
    </form>

    <form className="upload-form" onSubmit={handleSubmitUrl}>
      <div className="input-group">
        <label>Or enter a URL:</label>
        <input type="text" placeholder="https://..." value={url} onChange={handleUrlChange} />
      </div>
      <button type="submit">Analyze URL</button>
    </form>

    {message && <p className="server-message">{message}</p>}

    {diagramUrl && (
      <div className="diagram-wrapper">
        <div className="diagram-card">
          <h2 className="diagram-title">Your Kano Diagram</h2>
          <img src={diagramUrl} alt="Kano Diagram" className="diagram-image" />
          <a href="http://127.0.0.1:5000/download-diagram" download className="download-button">
            Download Diagram
          </a>
          <button onClick={handleSendEmail} className="email-button">
            Send Diagram by Email
          </button>
        </div>
      </div>
    )}
  </div>
</section>


      <footer className="footer">
        <p>2025 Kano Diagram Generator</p>
      </footer>
    </div>
  );
}

export default UploadPage;
