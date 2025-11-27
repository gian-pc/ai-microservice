from pydantic import BaseModel, Field
from typing import Literal

class ContentRequest(BaseModel):
    topic: str = Field(
        ...,
        min_length=3,
        max_length=500,
        example="Explícame qué es la Inteligencia Artificial"
    )
    tone: Literal["profesional", "casual", "técnico", "creativo"] = Field(
        default="profesional",
        description="Tono de la respuesta generada"
    )
    max_length: int = Field(
        default=300,
        ge=50,
        le=1000,
        description="Longitud máxima aproximada de la respuesta"
    )

class ContentResponse(BaseModel):
    generated_text: str
    latency: float = Field(description="Tiempo de generación en segundos")
