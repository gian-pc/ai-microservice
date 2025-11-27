import google.generativeai as genai
from app.config.settings import settings
import logging
import time
from typing import AsyncGenerator

logger = logging.getLogger(__name__)

# Configurar Gemini AI
genai.configure(api_key=settings.GEMINI_API_KEY)

async def generate_content_stream(
    topic: str,
    tone: str = "profesional",
    max_length: int = 300
) -> AsyncGenerator[str, None]:
    """
    Genera contenido con streaming usando async generator.

    Args:
        topic: El tema a generar
        tone: Tono de la respuesta (profesional, casual, técnico, creativo)
        max_length: Longitud máxima aproximada

    Yields:
        Chunks de texto generados en tiempo real
    """
    start_time = time.perf_counter()
    total_tokens = 0

    try:
        model = genai.GenerativeModel("models/gemini-flash-latest")

        # Prompt engineering con inyección dinámica de parámetros
        tone_instructions = {
            "profesional": "Responde de forma clara, objetiva y profesional.",
            "casual": "Responde de forma amigable, relajada y conversacional.",
            "técnico": "Usa terminología técnica precisa y explicaciones detalladas.",
            "creativo": "Sé creativo, usa metáforas y ejemplos interesantes."
        }

        prompt = f"""
{tone_instructions.get(tone, tone_instructions["profesional"])}

IMPORTANTE: Responde en UN SOLO PÁRRAFO CORTO de máximo {max_length} palabras. Sin listas, sin múltiples párrafos.

Tema: {topic}
"""

        logger.info(f"🚀 Iniciando stream | Tema: '{topic[:50]}...' | Tono: {tone}")

        # Streaming real con yield
        response = model.generate_content(prompt, stream=True)

        for chunk in response:
            if chunk.text:
                total_tokens += len(chunk.text.split())
                yield chunk.text

        # Logging al finalizar
        latency = time.perf_counter() - start_time
        logger.info(f"✅ Stream completado | Latencia: {latency:.2f}s | Tokens: ~{total_tokens}")

    except Exception as e:
        logger.error(f"❌ Error en streaming: {str(e)}")
        yield f"Error al generar contenido: {str(e)}"
