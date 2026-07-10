import React, { useRef, useState } from 'react';
import { UploadCloud, FileText, CheckCircle, Database, Trash2 } from 'lucide-react';

const Sidebar = ({ currentFile, onFileUpload, onDeleteFile }) => {
  const fileInputRef = useRef(null);
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);

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
      simulateUpload(files[0]);
    } else {
      alert('Please upload a valid document.');
    }
  };

  const handleFileChange = (e) => {
    const files = e.target.files;
    if (files.length > 0) {
      simulateUpload(files[0]);
    }
  };

  const simulateUpload = (file) => {
    setIsUploading(true);
    // Simulate network request to backend
    setTimeout(() => {
      onFileUpload(file);
      setIsUploading(false);
    }, 1500);
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
        <h3 style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', marginBottom: 'var(--spacing-md)', fontWeight: 500, textTransform: 'uppercase', letterSpacing: '0.05em' }}>
          Document Context
        </h3>
        
        {currentFile ? (
          <div className="document-item">
            <FileText size={24} color="var(--accent-primary)" style={{ flexShrinks: 0 }} />
            <div className="doc-info" style={{ flex: 1, minWidth: 0 }}>
              <span className="doc-name">{currentFile.name}</span>
              <span className="doc-status">
                <CheckCircle size={12} style={{ display: 'inline', verticalAlign: 'middle', marginRight: '4px' }} />
                Processed & Active
              </span>
            </div>
            <button 
              className="delete-btn" 
              onClick={onDeleteFile} 
              title="Remove document"
              aria-label="Remove document"
            >
              <Trash2 size={16} />
            </button>
          </div>
        ) : (
          <div style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', padding: 'var(--spacing-md)', backgroundColor: 'var(--bg-tertiary)', borderRadius: 'var(--radius-md)', border: '1px dashed var(--border-color)' }}>
            No document uploaded yet. Upload a document to begin chatting.
          </div>
        )}
      </div>

      <div 
        className={`upload-area ${isDragging ? 'drag-active' : ''}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
      >
        <UploadCloud className="upload-icon" size={40} />
        {isUploading ? (
          <span className="upload-title">Processing Document...</span>
        ) : (
          <>
            <span className="upload-title">Upload Knowledge Base</span>
            <span className="upload-text">Drag & drop or click to browse</span>
          </>
        )}
        <input 
          type="file" 
          ref={fileInputRef} 
          onChange={handleFileChange} 
          style={{ display: 'none' }} 
        />
      </div>
    </aside>
  );
};

export default Sidebar;
