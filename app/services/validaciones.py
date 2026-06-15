from datetime import date, time, datetime, timedelta
from app.models.reserva import Reserva
from app.models.servicio import Servicio
from app.models.cliente import Cliente
from app.exceptions import HorarioInvalidoError, AnticipacionInsuficienteError,SinDisponibilidadError, LimiteReservasActivasError

#Festivos en Colombia para el año actual

festivos_2026= {
    "2026-01-01", "2026-01-12", "2026-03-23", "2026-04-02", "2026-04-03",
    "2026-05-01", "2026-05-18", "2026-06-08", "2026-06-15", "2026-06-29",
    "2026-07-13", "2026-07-20", "2026-08-07", "2026-08-17", "2026-10-12",
    "2026-11-02", "2026-11-16", "2026-12-08", "2026-12-25"
}


def horario_valido(reserva:Reserva, servicio:Servicio):   
    # 1. Extraemos la fecha del objeto de reserva y la pasamos a formato texto para comparar
    fecha_str=reserva.fecha_servicio.strftime('%Y-%m-%d')
    # 2. Validación de Domingo (weekday == 6) usando el atributo correcto
    if reserva.fecha_servicio.weekday() ==6: #Dia Domingo
        raise HorarioInvalidoError ("La fecha solicitada corresponde a domingo.")
    # 3. Validación de día festivo
    if fecha_str in festivos_2026: 
        raise HorarioInvalidoError ("La fecha solicitada corresponde a festivo.")
    
    # 4. Validación de hora inicio y fin dentro del rango de servicios (entre 07:00 y 19:00 (hora America/Bogota))

    #Se establecen las horas de apertura y cierre:    
    hora_apertura = time(7,0)
    hora_cierre= time(19, 0)
    #Se extrae la duración del servicio y ser transforma en horas
    duracion_horas= max(1, int(servicio.duracion/60))
    #Se aplica ajuste para poder realizar el cálculo de la hora máxima de inicio, de manera que de acuerdo con la duración no 
    #exceda la hora del cierre (19:00)
    ajuste_cierre=  datetime.combine(date.today(), hora_cierre)
    # Restamos la duración real del servicio al objeto datetime de cierre para calcular el límite de inicio. [STEM-1]
    datetime_maxima = ajuste_cierre - timedelta(hours=duracion_horas)
    # Extraemos únicamente el objeto time resultante (HH:MM) descartando la fecha de apoyo.
    hora_maxima= datetime_maxima.time()

    # Valida si la hora de inicio es antes de la apertura
    if reserva.hora_inicio < hora_apertura:
        raise HorarioInvalidoError ("El horario solicitado está fuera del rango permitido de apertura (7:00 am)")
    # Valida si la hora de inicio es muy tarde respecto a la duración del servicio y hora de cierre (19:00)
    # Ninguna reserva deberá culminar después de la hora de cierre
    if reserva.hora_inicio > hora_maxima:
        raise HorarioInvalidoError ("El horario solicitado excede el máximo según la duración del servicio")
    if reserva.hora_fin > hora_cierre:
        raise HorarioInvalidoError ("El horario solicitado está fuera del rango permitido de cierre (19:00)")
    # Si pasa los filtros satisfactoriamente, la fecha y hora se ajustan a la regla
    return True

# Validación de anticipación mínima de 2 horas:

def anticipacion(reserva:Reserva):      
    # Captura del instante en el que se está realizando la reserva
    instante=datetime.now()
    #Combinación de fecha y hora del inicio del servicio
    inicio_servicio=  datetime.combine(reserva.fecha_servicio, reserva.hora_inicio)
    #Cálculo de la diferencia en horas entre el momento de la reserva y el inicio del servicio
    diferencia= inicio_servicio-instante
    #Validaciónd el resultado para aprobar o no la reserva
    if diferencia < timedelta(hours=2):
        raise AnticipacionInsuficienteError(
            f"Operación rechazada. Las reservas deben agendarse con un mínimo de 2 horas de anticipación. "
            f"Momento actual del sistema: {instante.strftime('%H:%M')}. "
            f"Hora solicitada: {reserva.hora_inicio.strftime('%H:%M')}."
        )
        
    return True


# Solapamientos

def validar_disponibilidad(reserva: Reserva, servicio: Servicio, historial_reservas: list[Reserva]):
    ocupacion = 0
    for r in historial_reservas:
        if (r.id_servicio == reserva.id_servicio and
            r.id_prestador == reserva.id_prestador and
            r.fecha_servicio == reserva.fecha_servicio and
            r.estado == "activa"):           
            if reserva.hora_inicio < r.hora_fin and reserva.hora_fin > r.hora_inicio:
                ocupacion += 1                

    if ocupacion >= servicio.capacidad:
        raise SinDisponibilidadError("Conflicto de agenda, el prestador {reserva.id_prestador} ya no cuenta con disponibilidad ")
    return True

#Cancelaciones y reembolsos:

def calcular_reembolso_cancelacion(reserva: Reserva, servicio: Servicio, cliente: Cliente) -> dict:
    # 1. Filtro de Catálogo: Si el servicio es NO reembolsable de origen, devuelve 0.0 de inmediato
    if getattr(servicio, "is_non_refundable", False) is True:
        reserva.monto_reembolso = 0.0
        return {"monto_reembolso": 0.0, "porcentaje_aplicado": "0% (No Reembolsable)"}

    # 2. Calcular tiempo restante hasta el inicio del servicio
    instante = datetime.now()
    inicio_servicio = datetime.combine(reserva.fecha_servicio, reserva.hora_inicio)
    diferencia = inicio_servicio - instante # [STEM-1]
    
    # Inicializamos la variable del cálculo
    reembolso = 0.0

    
    # LÓGICA DE REEMBOLSOS BASADA EN ANTICIPACIÓN Y TIPO DE CLIENTE
    
    # CASO A: Más de 24 horas de anticipación -> 100% Reembolso para TODOS
    if diferencia >= timedelta(hours=24):
        reembolso = servicio.costo_servicio
        porcentaje = "100%"

    # CASO B: Entre 4 y 24 horas de anticipación 
    elif timedelta(hours=4) <= diferencia < timedelta(hours=24):
        
        # Clientes Premium reciben 100%, Estándar reciben 50%
        if cliente.is_premium :
            reembolso= reserva.total_pagado
            porcentaje = "100% (Premium)"
        else:
            reembolso = reserva.total_pagado / 2
            porcentaje = "50% (Estándar)"

    # CASO C: Entre 1 y 4 horas de anticipación
    elif timedelta(hours=1) <= diferencia < timedelta(hours=4):
        # Clientes Premium reciben 50%, Estándar reciben 0%
        if cliente.is_premium :
            reembolso= reserva.total_pagado / 2
            porcentaje = "50% (Premium)"
        else:
            reembolso = 0.0
            porcentaje = "0% (Estándar)"

    # CASO D: Menos de 1 hora de anticipación -> 0% para TODOS
    else:
        reembolso = 0.0
        porcentaje = "0% "

    # 3. Asignamos el valor final redondeado al atributo de la reserva
    reserva.monto_reembolso = round(reembolso, 2)
    
    # Retornamos ambos valores en un diccionario para tu revisión
    return {
        "monto_reembolso": reserva.monto_reembolso,
        "porcentaje_aplicado": porcentaje
    }

# Limite de reservas por usuario: No más de 3 citas en estado activo

def validar_limite_reservas_cliente(nueva_reserva: Reserva, historial_reservas: list[Reserva]):
    # 1. Contamos linealmente cuántas reservas activas acumuladas tiene este cliente
    total_activas = 0
    
    for r in historial_reservas:
        if r.id_cliente == nueva_reserva.id_cliente and r.estado == "activa":
            total_activas += 1
            
    # 2. REGLA DE NEGOCIO: Si ya tiene 3 o más en estatus 'activa', bloqueamos la transacción
    if total_activas >= 3:
        raise LimiteReservasActivasError(
            f"El cliente con ID {nueva_reserva.id_cliente} ya tiene 3 reservas activas en el sistema. "
            "No se permiten registros adicionales hasta que libere un cupo."
        )
        
    return True
