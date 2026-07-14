from fastapi import APIRouter, UploadFile, File, Form, HTTPException
import os

# add_documents ko sahi se use karne ke liye call karenge
from app.rag.document_loader import load_and_split
from app.rag.vectorstore import add_documents, get_qdrant_client

router = APIRouter(prefix="/upload", tags=["Upload"])


@router.post("/")
async def upload_file(
    session_id: str = Form(...),
    file: UploadFile = File(...)
):
    try:
        # 1. Read uploaded file bytes
        file_bytes = await file.read()

        # 2. Load & split document into chunks
        documents = load_and_split(file_bytes, file.filename)

        if not documents:
            raise HTTPException(
                status_code=400, 
                detail="Document content could not be parsed or split."
            )

        # 3. Store embeddings in Qdrant using the correct function
        # Yeh function documents ko embed karke session_id wali collection mein daal dega
        add_documents(session_id, documents) 

        return {
            "success": True,
            "message": "Document uploaded and stored successfully.",
            "session_id": session_id,
            "filename": file.filename,
            "chunks": len(documents)
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    

@router.get('/cross')
def check_works():  # Fixed typo in function name
    # Health check for Qdrant client connection
    client = get_qdrant_client()
    try:
        # Sirf client object return karne ke bajay ek chota sa ping/check response dena reliable hota hai
        collections = client.get_collections()
        return {
            'status': 'Connected successfully',
            'available_collections': [c.name for c in collections.collections]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Qdrant connection failed: {str(e)}")