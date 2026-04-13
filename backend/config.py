from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    GROQ_API_KEY: str = ""
    CAL_COM_LINK: str = "https://cal.com/utkersh-basnet"
    CHROMA_PERSIST_DIR: str = "./chroma_db"
    CHAT_MODEL: str = "llama-3.3-70b-versatile"
    VOICE_MODEL: str = "llama-3.1-8b-instant"
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    VAPI_API_KEY: str = ""
    TWILIO_ACCOUNT_SID: str = ""
    TWILIO_AUTH_TOKEN: str = ""
    TWILIO_PHONE_NUMBER: str = ""
    CAL_COM_API_KEY: str = ""
    CAL_COM_EVENT_TYPE_ID: int = 0
    CAL_COM_USERNAME: str = ""
    DATA_DIR: str = "./data"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
