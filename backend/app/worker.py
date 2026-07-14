import os
from celery import Celery
from app.rag.document_loader import load_and_split
from app.rag.vectorstore import add_documents

# Read Redis URL from environment or fallback
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "rag_worker",
    broker=REDIS_URL,
    backend=REDIS_URL
)

# Optional configuration
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],  
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

@celery_app.task(bind=True, name="process_document_task")
def process_document_task(self, session_id: str, file_path: str, filename: str):
    """
    Background task to process large PDF files.
    """
    try:
        self.update_state(state='PROCESSING', meta={'status': 'Reading file'})
        # Read file bytes from temporary location
        with open(file_path, "rb") as f:
            file_bytes = f.read()

        self.update_state(state='PROCESSING', meta={'status': 'Splitting document'})
        documents = load_and_split(file_bytes, filename)
        
        if not documents:
            raise ValueError("Document content could not be parsed or split.")

        self.update_state(state='PROCESSING', meta={'status': 'Embedding and storing'})
        add_documents(session_id, documents)
        
        # Cleanup temporary file
        if os.path.exists(file_path):
            os.remove(file_path)

        return {
            "success": True, 
            "message": "Document processed successfully", 
            "chunks": len(documents)
        }
    except Exception as e:
        # Cleanup on failure too
        if os.path.exists(file_path):
            os.remove(file_path)
        raise Exception(f"Failed to process document: {str(e)}")
