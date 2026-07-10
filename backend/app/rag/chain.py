import os
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore  
# Load environment variables
load_dotenv()

# ==========================
# 1. LOAD DOCUMENT
# ==========================
raw_text = """Mahatma Gandhi was born on 2 October 1869 in Porbandar, Gujarat.
His full name was Mohandas Karamchand Gandhi.
He was known as the "Father of the Nation" in India.
Gandhi ji followed the principles of truth and non-violence.
He played an important role in India's freedom struggle.
He led movements like the Non-Cooperation Movement and Quit India Movement.
He inspired people through his simple lifestyle and strong beliefs.
Gandhi ji fought against injustice and supported equality.
India got independence on 15 August 1947, after a long freedom movement.
Mahatma Gandhi was assassinated on 30 January 1948, but his ideas continue to inspire the world."""

documents = [Document(page_content=raw_text, metadata={"source": "gandhi_history"})]

print("Documents loaded:", len(documents))

# ==========================
# 2. SPLIT DOCUMENT
# ==========================
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50
)

chunks = text_splitter.split_documents(documents)

print("Total chunks:", len(chunks))
for i, chunk in enumerate(chunks):
    print(f"Chunk {i+1} size: {len(chunk.page_content)} chars")

# ==========================
# 3. CREATE EMBEDDING MODEL
# ==========================
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001"
)

from app.config.setting import getappconfig
config =getappconfig()


# ==========================
# 4. STORE INTO QDRANT (FOOLPROOF METHOD)
# ==========================
from qdrant_client import QdrantClient

print("\nConnecting to Qdrant Database...")

# 1. Sabse pehle khud connection banna hai taaki memory me save na ho
client = QdrantClient(url=config.QDRANT_URL)

# 2. VectorStore ko batao ki isi client (Docker) ke andar kaam karna hai
vector_store = QdrantVectorStore(
    client=client,
    collection_name="my_documents",
    embedding=embeddings
)

print("Saving chunks into the database...")

# 3. Ab data add karo (yeh direct Docker me jayega)
vector_store.add_documents(chunks)

print("✅ Data stored successfully in Qdrant Docker!")