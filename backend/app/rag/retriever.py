
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from app.config.setting import getappconfig
from dotenv import load_dotenv

config = getappconfig()

load_dotenv()

def get_vector_store():
    """
    Yeh function Qdrant database se connection banata hai.
    """
    # 1. Same embedding model jo humne ingest.py me use kiya tha
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/text-embedding-004", 
        google_api_key=config.GEMINI_API_KEY
    )

    # 2. Qdrant Client Initialize karna
    client = QdrantClient(url=config.QDRANT_URL)

    # 3. Vector Store object create karna
    vector_store = QdrantVectorStore(
        client=client,
        collection_name="rag_documents", # Dhyan rahe, name ingest.py jaisa same ho
        embedding=embeddings,
    )
    
    return vector_store

def get_retriever(k: int = 4):
    """
    Yeh function vector store ko as a 'Retriever' return karta hai.
    k = 4 ka matlab hai ki yeh best 4 matching chunks nikal kar layega.
    """
    vector_store = get_vector_store()
    
    # search_type="similarity" by default hota hai
    # 'k' parameter batata hai ki top kitne results chahiye
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k}
    )
    return retriever

# Testing ke liye chota sa function (optional)
def search_documents(query: str, k: int = 4):
    """Direct search karne ke liye helper function"""
    try:
        retriever = get_retriever(k=k)
        results = retriever.invoke(query)
        return results
    except Exception as e:
        print(f"Error during retrieval: {e}")
        return []