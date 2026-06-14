from fastapi import APIRouter, HTTPException
from app.models.reserva import Reserva
from app.db import cargar_seed 
from app.services.validaciones import (
    horario_valido, 
    anticipacion, 
    validar_disponibilidad,  
    validar_limite_reservas_cliente,
    calcular_reembolso_cancelacion
)

router = APIRouter(prefix="/reservas", tags=["Reservas"])

# Cargamos el estado inicial en memoria desde el archivo seed.json
CLIENTES, PRESTADORES, SERVICIOS, RESERVAS = cargar_seed()

# =========================================================================
# ENDPOINT: CREAR NUEVA RESERVA
# =========================================================================
@router.post("/", status_code=201)
def crear_nueva_reserva(nueva_reserva: Reserva):
    try:
        # 1. Recuperamos el contexto del servicio desde el catálogo 
        servicio = SERVICIOS.get(nueva_reserva.id_servicio)
        if not servicio:
            raise HTTPException(status_code=404, detail="El servicio solicitado no existe.")
            
        # 2. Ejecutar la batería de reglas de negocio en el orden correcto
        horario_valido(nueva_reserva, servicio)
        anticipacion(nueva_reserva)
        validar_limite_reservas_cliente(nueva_reserva, RESERVAS)
        validar_disponibilidad(nueva_reserva, servicio, RESERVAS)
        
        # 3. Guardar en el historial transaccional
        RESERVAS.append(nueva_reserva)
        return {"mensaje": "Reserva registrada con éxito", "data": nueva_reserva}
        
    except Exception as e:
        # Capturar cualquier excepción de negocio y la devuelve limpia al cliente
        raise HTTPException(status_code=400, detail=str(e))

# =========================================================================
# ENDPOINT: CANCELAR RESERVA EXISTENTE
# =========================================================================
@router.post("/{id_reserva}/cancelar")
def cancelar_reserva_existente(id_reserva: int):
    # 1. Buscar la reserva en la lista en memoria
    reserva = next((r for r in RESERVAS if r.id_reserva == id_reserva), None)
    if not reserva:
        raise HTTPException(status_code=404, detail="La reserva solicitada no existe.")
        
    if reserva.estado == "cancelada":
        raise HTTPException(status_code=400, detail="Esta reserva ya se encuentra cancelada.")
        
    # 2. Obtener las entidades relacionadas para aplicar las matemáticas financieras
    servicio = SERVICIOS.get(reserva.id_servicio)
    cliente = CLIENTES.get(reserva.id_cliente)
    
    # 3. Calcular la matriz con tu función que devuelve el dict
    auditoria_reembolso = calcular_reembolso_cancelacion(reserva, servicio, cliente)
    
    # CONTROL DE SEGURIDAD: Manejar si la función devolvió un float plano (0.0) en lugar de dict
    if isinstance(auditoria_reembolso, float):
        monto = auditoria_reembolso
        porcentaje = "0% (No Reembolsable)"
    else:
        monto = auditoria_reembolso["monto_reembolso"]
        porcentaje = "0%" if "porcentaje_aplicado" not in auditoria_reembolso else auditoria_reembolso["porcentaje_aplicado"]
    
    # 4. Modificar el estatus de la reserva en la memoria
    reserva.estado = "cancelada"
    
    return {
        "mensaje": "Reserva cancelada exitosamente",
        "monto_reembolsado": monto,
        "porcentaje_aplicado": porcentaje
    }
