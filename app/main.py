from fastapi import FastAPI
from app.routers.reservas import router as reservas_router

# 1. Inicializar la aplicación de FastAPI con metadatos profesionales
app = FastAPI(
    title="Booking API - Sistema de Reservas",
    description="API REST robusta con capa defensiva para validación de reglas de negocio y reembolsos.",
    version="1.0.0"
)

# 2. Conectar el router de reserva
app.include_router(reservas_router)

# 3. Endpoint base de bienvenida para verificar que la API responda en el navegador
@app.get("/")
def leer_raiz():
    return {
        "sistema": "Booking API Activa",
        "estado": "Operando de forma consistente",
        "documentacion": "/docs"
    }
