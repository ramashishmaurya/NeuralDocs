<div align="center">
  <img src="https://via.placeholder.com/1200x300/0f172a/38bdf8?text=NexusRAG+|+Intelligent+Document+Chat" alt="NexusRAG Banner" />

  <h1>🧠 NexusRAG</h1>
  
  <p><strong>A highly optimized, full-stack Retrieval-Augmented Generation (RAG) engine.</strong></p>

  <p>
    <img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" alt="React" />
    <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" alt="FastAPI" />
    <img src="https://img.shields.io/badge/Celery-37814A?style=for-the-badge&logo=celery&logoColor=white" alt="Celery" />
    <img src="https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white" alt="Redis" />
    <img src="https://img.shields.io/badge/LangChain-121212?style=for-the-badge&logo=chainlink&logoColor=white" alt="LangChain" />
    <img src="https://img.shields.io/badge/Qdrant-FF5252?style=for-the-badge&logo=qdrant&logoColor=white" alt="Qdrant" />
    <img src="https://img.shields.io/badge/Ollama-ffffff?style=for-the-badge&logo=ollama&logoColor=black" alt="Ollama" />
  </p>
</div>

---

## 📖 Overview

**NexusRAG** is a production-ready web application designed to allow users to interact dynamically with complex documents. By combining the conversational reasoning of **Ollama LLM (qwen2.5 / llama3)** with the ultra-fast semantic search of a **Qdrant Vector Database**, this app accurately grounds AI responses in your personal data. 

Built with performance in mind, the architecture completely avoids traditional HTTP polling in favor of **WebSocket streaming**, reducing the Time-To-First-Token (TTFT) and delivering a real-time typing experience to the user.

---

## ✨ Technical Highlights

- **⚡ WebSocket Streaming:** Implements asynchronous generators via LangChain's `.astream()` piped directly into a FastAPI WebSocket, rendering text to the React frontend instantly chunk-by-chunk.
- **🧠 History-Aware Retrieval:** Incorporates contextual compression. If a user asks a follow-up question, the backend automatically reformulates the query based on chat history before querying the vector space.
- **🗃️ Advanced Vector Management:** Global instance caching for both Qdrant Cloud clients and embedding models to eliminate cold-start overhead during multi-turn conversations.
- **📄 Multi-Format Processing:** Out-of-the-box support for chunking, parsing, and cleaning `.pdf`, `.docx`, and `.txt` files.

---

## 🏗️ System Architecture

1. **Ingestion Pipeline:** File Upload → PyPDF/Docx Parser → Recursive Character Text Splitter (500 chunk size / 50 overlap) → Ollama Embeddings (nomic-embed-text) → Qdrant Vector Store.
2. **Retrieval Pipeline:** User Query + Session ID → WebSocket Connection → Chat History Retrieval → Query Reformulation → Qdrant Similarity Search (k=4) → Context injection into Ollama LLM.

### Architecture Data Flow

```mermaid
graph TD
    %% Styles
    classDef frontend fill:#3b82f6,stroke:#2563eb,stroke-width:2px,color:white;
    classDef backend fill:#10b981,stroke:#059669,stroke-width:2px,color:white;
    classDef database fill:#f59e0b,stroke:#d97706,stroke-width:2px,color:white;
    classDef ai fill:#8b5cf6,stroke:#7c3aed,stroke-width:2px,color:white;
    classDef broker fill:#ef4444,stroke:#dc2626,stroke-width:2px,color:white;

    %% -------------------------------------
    %% 1. Document Upload Flow (Async)
    %% -------------------------------------
    subgraph "Async Document Upload Flow"
        U1["User Uploads PDF (React)"]:::frontend
        U2["FastAPI Upload Route"]:::backend
        U3[("Redis (Celery Broker)")]:::broker
        U4["Celery Background Worker"]:::backend
        U5["LangChain PyPDFLoader"]:::backend
        U6["RecursiveCharacterTextSplitter"]:::backend
        U7["Ollama Embeddings"]:::ai
        DB[("Qdrant Vector DB")]:::database
        
        U1 -->|"1. Send PDF"| U2
        U2 -->|"2. Save to Temp & Trigger Task"| U3
        U2 -.->|"3. Return Task ID Immediately"| U1
        U3 -->|"4. Pick up Task"| U4
        U4 --> U5
        U5 --> U6
        U6 -->|"Chunks"| U7
        U7 -->|"Vector Embeddings"| DB
    end

    %% -------------------------------------
    %% 2. Chat & RAG Flow
    %% -------------------------------------
    subgraph "Real-Time Chat & RAG Flow (Continuous)"
        C1["User Asks Question (React)"]:::frontend
        C2["WebSocket Route (chat.py)"]:::backend
        C3["Pipeline (pipeline.py)"]:::backend
        C4[("Redis (Chat History & LLM Cache)")]:::broker
        C5["LangChain Prompt Template"]:::backend
        C6["Ollama LLM (qwen2.5:latest)"]:::ai

        C1 -- "1. Sends Query (JSON)" --> C2
        C2 --> C3
        
        C3 -->|"2. Check Cache & Fetch History"| C4
        C4 -.->|"Cache Hit (Fast Return)"| C3
        
        C3 -->|"3. Search Similar Text"| DB
        DB -.->|"Returns Top 4 Paragraphs"| C3
        
        C3 -->|"4. Combine Question + Context"| C5
        C5 -->|"5. Send Context"| C6
        
        C6 -.->|"6. Generate Stream (Word-by-Word)"| C3
        C3 -- "7. Stream Chunks to Frontend" --> C1
    end
```

---

## 🚀 Getting Started

Follow these instructions to spin up the local development environment.

### Prerequisites

* **Node.js** (v18+) and **npm**
* **Python** (v3.10+)
* API Keys for [Google Gemini](https://aistudio.google.com/) and [Qdrant Cloud](https://cloud.qdrant.io/).

### 1. Backend Setup (FastAPI)

```bash
# Navigate to the backend directory
cd backend

# Create and activate a virtual environment
python -m venv myenv
source myenv/bin/activate  # Windows: myenv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn langchain langchain-google-genai langchain-qdrant qdrant-client python-dotenv pypdf docx2txt

# Configure Environment Variables
echo 'GOOGLE_API_KEY="your_api_key_here"' >> .env
echo 'QDRANT_URL="your_qdrant_url_here"' >> .env
echo 'QDRANT_API_KEY="your_qdrant_api_key"' >> .env

# Run the server
uvicorn main:app --reload
```

### 2. Frontend Setup (React/Vite)

```bash
# Navigate to the frontend directory
cd frontend/chat-app

# Install dependencies
npm install

# Start the Vite development server
npm run dev
```

Your frontend should now be running on `http://localhost:5173`!

---

## 🧠 Future Roadmap

- [x] **Redis Integration:** Swap in-memory python dictionaries for Redis to persist chat history across server restarts and scale horizontally.
- [x] **LLM Caching:** Implement LLM response caching to return instant answers for frequently asked questions, saving API costs.
- [x] **Celery Task Queue:** Offload heavy PDF embedding tasks to background workers to handle massive 1000+ page documents seamlessly.
- [ ] **User Authentication (JWT/OAuth2):** Implement secure login so multiple users can have their own private document workspaces and chat histories.
- [ ] **Multi-Modal RAG (Vision):** Upgrade the parser to extract and understand images, tables, and diagrams from PDFs using Vision models.
- [ ] **GraphRAG (Knowledge Graphs):** Integrate Neo4j to build knowledge graphs from documents for understanding complex relationships between entities.
- [ ] **Internet Search Fallback:** Automatically search the web (e.g., via DuckDuckGo API) if the answer is not found in the uploaded documents.

---

<div align="center">
  <p>Built with ❤️ by an aspiring Full Stack AI Developer.</p>
</div>
