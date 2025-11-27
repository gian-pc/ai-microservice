from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from app.routes.content_routes import router as content_router
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%H:%M:%S'
)

app = FastAPI(
    title="AI Content Microservice",
    description="Microservicio profesional con FastAPI + Gemini AI",
    version="1.0.0"
)

# Configurar CORS
# NOTA: En producción, reemplaza ["*"] con dominios específicos
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Cambiar a dominios específicos en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar rutas
app.include_router(content_router, prefix="/api/v1/content", tags=["Content"])

# Servir archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_root():
    return FileResponse("static/index.html")

@app.get("/health")
async def health_check():
    """Health check endpoint para monitoreo."""
    return {"status": "healthy", "service": "AI Content Microservice"}
