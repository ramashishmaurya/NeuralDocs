import os
from dotenv import load_dotenv
# pyrefly: ignore [missing-import]
from langchain_ollama import OllamaEmbeddings
from langchain_qdrant import QdrantVectorStore
# pyrefly: ignore [missing-import]
from qdrant_client import QdrantClient
# pyrefly: ignore [missing-import]
from app.config.setting import getappconfig

config = getappconfig()
# Environment variables load karein
load_dotenv()

_embeddings = None
_qdrant_client = None

def get_embeddings():
    """Return Ollama Embeddings (Cached)"""
    global _embeddings

    if _embeddings is None:
        _embeddings = OllamaEmbeddings(
            model="nomic-embed-text:latest" ,
            base_url="http://localhost:11434"
        )

    return _embeddings

def get_qdrant_client():
    """Sirf client chahiye toh yeh call karna (Cached)"""
    global _qdrant_client
    if _qdrant_client is None:
        _qdrant_client = QdrantClient(
            url=os.getenv("QDRANT_URL"),
            api_key=os.getenv("QDRANT_API_KEY")
        )
    return _qdrant_client

def get_or_create_collection(session_id: str) -> QdrantVectorStore:
    """
    Yeh function sirf session_id lega aur Qdrant collection ka instance return karega.
    Iska use tere 'build_rag_chain' mein retriever banane ke liye hoga (bina document bheje).
    """
    # Direct QdrantVectorStore return kar rahe hain cached clients ke saath
    return QdrantVectorStore(
        client=get_qdrant_client(),
        collection_name=session_id,
        embedding=get_embeddings()
    )

def add_documents(session_id: str, documents:list[str]):
    """
    Yeh function sirf tab call karna jab naye documents ko embed karke 
    Qdrant mein save karna ho.
    """
    # from_documents documents ko embed karke directly collection mein daal dega
    vectorstore = QdrantVectorStore.from_documents(
        documents=documents,
        embedding=get_embeddings(),
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY"),
        collection_name=session_id,
    )

    print(f"✅ Data successfully stored/updated in Qdrant collection: '{session_id}'")
    return vectorstore

