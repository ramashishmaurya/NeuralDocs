from fastapi import APIRouter, UploadFile, File, Form, HTTPException
import os
import uuid
import shutil
from celery.result import AsyncResult
from app.worker import process_document_task
from app.rag.vectorstore import get_qdrant_client

router = APIRouter(prefix="/upload", tags=["Upload"])

UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/")
async def upload_file(
    session_id: str = Form(...),
    file: UploadFile = File(...)
):
    try:
        # Generate a unique temp file path
        temp_filename = f"{uuid.uuid4()}_{file.filename}"
        temp_file_path = os.path.join(UPLOAD_DIR, temp_filename)
        
        # Save uploaded file to temp directory
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Trigger Celery Task asynchronously
        task = process_document_task.delay(session_id, temp_file_path, file.filename)

        return {
            "success": True,
            "message": "Document uploaded successfully and is being processed in the background.",
            "session_id": session_id,
            "task_id": task.id
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.get('/status/{task_id}')
def check_task_status(task_id: str):
    task = AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'status': 'Task is waiting in queue...'
        }
    elif task.state == 'PROCESSING':
        response = {
            'state': task.state,
            'status': task.info.get('status', 'Processing...')
        }
    elif task.state == 'SUCCESS':
        response = {
            'state': task.state,
            'status': 'Completed',
            'result': task.info
        }
    elif task.state == 'FAILURE':
        response = {
            'state': task.state,
            'status': 'Failed',
            'error': str(task.info)
        }
    else:
        response = {
            'state': task.state,
            'status': str(task.info)
        }
    return response

# this is for ckekc wheather session is stored in qdrant database or not 
@router.get('/cross')
def check_works(): 
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