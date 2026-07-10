from qdrant_client import QdrantClient

from app.config.setting import getappconfig

config = getappconfig()

client = QdrantClient(
    url= config.QDRANT_URL , 
    api_key=config.QDRANT_API_KEY
)