
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.chat import router as chat_router
from app.api.routes.upload import router as upload_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Development only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(upload_router)
app.include_router(chat_router)

