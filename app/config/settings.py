from pydantic_settings import BaseSettings
from pydantic import field_validator

class Settings(BaseSettings):
    GEMINI_API_KEY: str

    @field_validator('GEMINI_API_KEY')
    @classmethod
    def validate_api_key(cls, v: str) -> str:
        if not v or v.strip() == "":
            raise ValueError("GEMINI_API_KEY no puede estar vacía")
        if len(v) < 20:
            raise ValueError("GEMINI_API_KEY parece inválida (muy corta)")
        return v

    class Config:
        env_file = ".env"

settings = Settings()
