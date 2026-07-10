from pydantic_settings import BaseSettings , SettingsConfigDict

from functools import lru_cache


class AppConfig(BaseSettings):
    GOOGLE_API_KEY : str 
    QDRANT_URL : str 
    QDRANT_API_KEY : str 




    model_config = SettingsConfigDict(
        env_file='.env'
    )
@lru_cache
def getappconfig():
    return AppConfig() 