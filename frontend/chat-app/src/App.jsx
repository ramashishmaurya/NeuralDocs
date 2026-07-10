import React, { useState } from 'react';
import Sidebar from './components/Sidebar';
import ChatInterface from './components/ChatInterface';
import './App.css';

function App() {
  const [currentFile, setCurrentFile] = useState(null);

  const handleFileUpload = (file) => {
    setCurrentFile(file);
    // In a real application, you would send this file to your backend here
    console.log('File ready for backend:', file.name);
  };

  const handleDeleteFile = () => {
    setCurrentFile(null);
    console.log('File deleted from frontend state.');
  };

  return (
    <div className="app-container">
      <Sidebar 
        currentFile={currentFile} 
        onFileUpload={handleFileUpload} 
        onDeleteFile={handleDeleteFile}
      />
      <ChatInterface 
        currentFile={currentFile} 
      />
    </div>
  );
}

export default App;
