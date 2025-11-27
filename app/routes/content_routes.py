from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.schemas.content_schema import ContentRequest
from app.services.content_service import generate_content_stream
import time

router = APIRouter()

@router.post("/stream")
async def create_content_stream(payload: ContentRequest):
    """
    Endpoint de streaming real - Respuesta token por token (efecto máquina de escribir).

    Ventajas:
    - TTFB (Time To First Byte) reducido de ~20s a ~2s
    - Mejor UX: el usuario ve progreso inmediato
    - Libera el event loop: no bloquea otros requests
    """
    try:
        return StreamingResponse(
            generate_content_stream(
                topic=payload.topic,
                tone=payload.tone,
                max_length=payload.max_length
            ),
            media_type="text/plain",
            headers={
                "Cache-Control": "no-cache",
                "X-Content-Type-Options": "nosniff",
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/")
async def create_content_blocking(payload: ContentRequest):
    """
    Endpoint sin streaming - Espera la respuesta completa (para comparación).

    Desventajas:
    - Bloquea el thread hasta recibir toda la respuesta
    - TTFB alto (~20-30 segundos)
    - Peor UX: usuario espera viendo loading
    """
    try:
        start_time = time.perf_counter()

        # Recolectar todos los chunks en memoria
        full_text = ""
        async for chunk in generate_content_stream(
            topic=payload.topic,
            tone=payload.tone,
            max_length=payload.max_length
        ):
            full_text += chunk

        latency = time.perf_counter() - start_time

        return {
            "generated_text": full_text,
            "latency": round(latency, 2)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
