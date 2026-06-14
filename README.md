# booking-api


Este proyecto implementa una API REST de alto rendimiento utilizando **FastAPI** y **Pydantic V2** para la gestión integrada de agendas, control estricto de reglas operativas locales y políticas financieras de reembolsos transaccionales.

## Instrucciones de Instalación y Ejecución

1. **Activar el entorno virtual**:
   ```bash
   .venv\Scripts\activate
   ```
2. **Instalar dependencias del sistema**:
   ```bash
   pip install fastapi uvicorn pydantic email-validator faker pytest
   ```
3. **Ejecutar el servidor de desarrollo**:
   ```bash
   uvicorn app.main:app --reload
   ```
4. **Acceder a la documentación interactiva**:
   Abre tu navegador en: http://127.0.0.1:8000/docs

## Decisiones Técnicas y Arquitectura

- **Arquitectura Multicapa Defensiva**: Se diseñó una separación clara de responsabilidades. La primera capa delega en Pydantic el parsing sintáctico y la validación de tipos nativos (`date`, `time`). La segunda capa, aislada en un módulo de servicios de negocio (`app/services/validaciones.py`), gestiona las reglas dinámicas y relacionales de la plataforma.
- **Ecosistema Indexado en RAM**: Ante la restricción de persistencia, los catálogos estáticos se indexaron como diccionarios en memoria basados en su ID, asegurando lecturas instantáneas de complejidad constante **O(1)**. El historial de reservas se maneja como listas dinámicas para auditorías secuenciales en tiempo de ejecución.
- **Validación de Solapamiento por Capacidad**: La agenda de profesionales no es un bloqueo booleano rígido. El sistema calcula dinámicamente la intersección horaria acumulando cupos concurrentes en tiempo real para soportar de forma nativa servicios grupales (con capacidad > 1) y citas exclusivas (con capacidad = 1).
- **Manejo de Tiempos en Vivo**: Las validaciones de anticipación mínima y los porcentajes financieros de reembolso por cancelación computan la holgura temporal en tiempo real empleando restas mediante objetos `timedelta`, blindando el backend contra registros extemporáneos.

#Luis Guillermo Ramirez