from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from app.models.schemas import ChatRequest, ChatResponse
from app.rag.pipeline import ask_question, stream_ask_question
import json
 
router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        answer, sources = ask_question(request.session_id, request.question)
        return ChatResponse(
            answer=answer,
            sources=sources,
            session_id=request.session_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Receive data from client
            data = await websocket.receive_text()
            try:
                payload = json.loads(data)
                session_id = payload.get("session_id")
                question = payload.get("question")
                
                if not session_id or not question:
                    await websocket.send_text(json.dumps({"error": "Missing session_id or question"}))
                    continue
                
                # Stream response
                async for chunk in stream_ask_question(session_id, question):
                    await websocket.send_text(json.dumps({"chunk": chunk}))
                    
                # Signal completion
                await websocket.send_text(json.dumps({"done": True}))
                
            except json.JSONDecodeError:
                await websocket.send_text(json.dumps({"error": "Invalid JSON payload"}))
                
    except WebSocketDisconnect:
        print("Client disconnected from chat websocket")
    except Exception as e:
        print(f"WebSocket Error: {e}")