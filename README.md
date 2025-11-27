# AI Content Microservice

Microservicio profesional de generación de contenido con IA utilizando **FastAPI** y **Google Gemini**.

## Características

- API REST con FastAPI
- Integración con Google Gemini AI
- Frontend web interactivo
- Arquitectura modular y escalable
- CORS habilitado
- Documentación automática (Swagger)

## Estructura del Proyecto

```
ai-microservice/
├── app/
│   ├── config/          # Configuración
│   ├── routes/          # Endpoints de la API
│   ├── schemas/         # Modelos Pydantic
│   └── services/        # Lógica de negocio
├── static/              # Frontend
├── main.py              # Punto de entrada
└── requirements.txt     # Dependencias
```

## Instalación

1. **Clonar el repositorio**

2. **Crear entorno virtual:**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno:**
```bash
cp .env.example .env
# Edita .env y agrega tu GEMINI_API_KEY
```

Obtén tu API key en: https://makersuite.google.com/app/apikey

## Uso

Iniciar el servidor:
```bash
uvicorn main:app --reload
```

El servicio estará disponible en:
- Frontend: http://localhost:8000
- API Docs: http://localhost:8000/docs

## API Endpoints

### GET /health
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "AI Content Microservice"
}
```

### POST /api/v1/content/stream
Genera contenido con streaming (recomendado).

**Request:**
```json
{
  "topic": "Inteligencia Artificial",
  "tone": "profesional",
  "max_length": 300
}
```

**Response:** Streaming de texto en tiempo real

### POST /api/v1/content/
Genera contenido sin streaming (para comparación).

**Request:**
```json
{
  "topic": "Inteligencia Artificial",
  "tone": "profesional",
  "max_length": 300
}
```

**Response:**
```json
{
  "generated_text": "Contenido generado por Gemini...",
  "latency": 5.23
}
```

## Tecnologías

- **FastAPI** - Framework web moderno y rápido
- **Google Gemini** - Modelo de IA generativa
- **Pydantic** - Validación de datos
- **Uvicorn** - Servidor ASGI

## Licencia

MIT
