import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

# Environment variables load karein
load_dotenv()

# Qdrant URL set karein
QDRANT_URL = os.getenv("QDRANT_URL")

def get_embeddings():
    """Gemini Embeddings return karega (jo humne fix kiya tha)"""
    return GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001"
    )

def get_or_create_collection(session_id: str) -> QdrantVectorStore:
    """
    Yeh function Qdrant se connect karega aur session_id ke naam ki 
    collection return karega. Agar collection nahi hogi toh Qdrant 
    khud usko add_documents call hone par create kar lega.
    """
    client = QdrantClient(url=QDRANT_URL)
    
    return QdrantVectorStore(
        client=client,
        collection_name=session_id, # Session ID hi Collection ka naam ban jayegi
        embedding=get_embeddings()
    )

def add_documents(session_id: str, documents):
    """
    Specific session_id wali collection mein chunks/documents save karega.
    """
    vectorstore = get_or_create_collection(session_id)
    vectorstore.add_documents(documents)
    
    print(f"✅ Data successfully stored in Qdrant collection: '{session_id}'")
    return vectorstore