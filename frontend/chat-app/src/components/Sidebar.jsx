import React, { useRef, useState } from "react";
import {
  UploadCloud,
  FileText,
  CheckCircle,
  Database,
  Trash2,
} from "lucide-react";

const Sidebar = ({ currentFile, onFileUpload, onDeleteFile }) => {
  const fileInputRef = useRef(null);

  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);

  // Create Session ID Once
  let sessionId = localStorage.getItem("session_id");

  if (!sessionId) {
    sessionId = crypto.randomUUID();
    localStorage.setItem("session_id", sessionId);
  }

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);

    const files = e.dataTransfer.files;

    if (files.length > 0) {
      uploadFile(files[0]);
    }
  };

  const handleFileChange = (e) => {
    const files = e.target.files;

    if (files.length > 0) {
      uploadFile(files[0]);
    }
  };

  const uploadFile = async (file) => {
    try {
      setIsUploading(true);

      const formData = new FormData();

      formData.append("session_id", sessionId);
      formData.append("file", file);

      const response = await fetch("http://127.0.0.1:8000/upload/", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Upload Failed");
      }

      const data = await response.json();

      console.log("Upload Response:", data);

      onFileUpload(file);

      alert("✅ File Uploaded Successfully");
    } catch (error) {
      console.error(error);
      alert("❌ Upload Failed");
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <h1 className="brand">
          <Database className="brand-icon" size={28} />
          NexusRAG
        </h1>
      </div>

      <div className="sidebar-content">
        <h3
          style={{
            fontSize: "0.875rem",
            color: "var(--text-secondary)",
            marginBottom: "var(--spacing-md)",
          }}
        >
          Document Context
        </h3>

        {currentFile ? (
          <div className="document-item">
            <FileText size={24} />

            <div className="doc-info">
              <span>{currentFile.name}</span>

              <span className="doc-status">
                <CheckCircle size={12} />
                Processed & Active
              </span>
            </div>

            <button onClick={onDeleteFile}>
              <Trash2 size={16} />
            </button>
          </div>
        ) : (
          <p>No document uploaded.</p>
        )}
      </div>

      <div
        className={`upload-area ${isDragging ? "drag-active" : ""}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current.click()}
      >
        <UploadCloud size={40} />

        {isUploading ? (
          <span>Uploading...</span>
        ) : (
          <>
            <span>Upload Knowledge Base</span>
            <span>Drag & Drop or Click</span>
          </>
        )}

        <input
          type="file"
          accept=".pdf,.docx,.txt"
          ref={fileInputRef}
          style={{ display: "none" }}
          onChange={handleFileChange}
        />
      </div>
    </aside>
  );
};

export default Sidebar;