from datetime import date, time, datetime, timedelta
from app.models.reserva import Reserva
from app.models.servicio import Servicio
from app.exceptions import HorarioInvalidoError
from app.services.validaciones import horario_valido, anticipacion

# 1. Creamos un servicio de prueba (Duración: 2 horas = 120 min)
servicio_test = Servicio(
    id_servicio=1,
    cod_servicio="B01",
    nombre_servicio="Catering",
    duracion=120,
    is_non_refundable=True,
    capacidad=50,
    id_prestador=2,
    costo_servicio=200.0
)



   

print("--- INICIANDO PRUEBAS DE ESCRITORIO ---")

# CASO 1: Probar un Domingo (Falla)
print("--- CASO 1: RESERVA DOMINGO  ---")
try:
    reserva_domingo = Reserva(
        id_reserva=1, id_cliente=1, id_servicio=1, id_prestador=2,
        fecha_reserva=date(2026, 6, 14),
        fecha_servicio=date(2026, 6, 14), # Hoy es Domingo 14 de Junio de 2026
        hora_inicio=time(10, 0), 
        hora_fin=time(12, 0),
        estado="activa", monto_reembolso=0.0, total_pagado=200.0
    )
    horario_valido(reserva_domingo, servicio_test)
except HorarioInvalidoError as e:
    print(f"❌ Prueba Domingo: Reserva rechazada: ({e})")

# CASO 2: Probar una reserva que termina después de las 19:00 (Falla)
print("--- CASO 2: SERVICIO TERMINA DESPUES DE LAS 19:00 ---")
try:
    reserva_tardia = Reserva(
        id_reserva=2, id_cliente=1, id_servicio=1, id_prestador=2,
        fecha_reserva=date(2026, 6, 14),
        fecha_servicio=date(2026, 6, 17), # Martes (Día válido)
        hora_inicio=time(18, 0),          # 6:00 PM + 2h de servicio = 20:00 (Se pasa)
        hora_fin=time(20, 0),
        estado="activa", monto_reembolso=0.0, total_pagado=200.0
    )
    horario_valido(reserva_tardia, servicio_test)
except HorarioInvalidoError as e:
    print(f"❌ Reserva rechazada:({e})")

# CASO 3: Probar un horario totalmente válido (OK)
print("--- CASO 3: HORARIO VÁLIDO ---")
try:
    reserva_valida = Reserva(
        id_reserva=3, id_cliente=1, id_servicio=1, id_prestador=2,
        fecha_reserva=date(2026, 6, 14),
        fecha_servicio=date(2026, 6, 17), # Lunes 15 de Junio
        hora_inicio=time(9, 0),            # 09:00 AM (Abre a las 7)
        hora_fin=time(11, 0),              # Termina 11:00 AM (Cierra a las 19)
        estado="activa", monto_reembolso=0.0, total_pagado=200.0
    )
    resultado = horario_valido(reserva_valida, servicio_test)
    if resultado:
        print("✅ Prueba Reserva Válida: Pasó con éxito (Retornó True)")
except Exception as e:
    print(f"🔴 Falló la prueba válida inesperadamente: {e}")

print("--- CASO 4: VALIDAR ANTICIPACIÓN DE 2 HORAS ---")
# CASO 4: Probar reserva sin anticipación
try:
    reserva_valida = Reserva(
        id_reserva=3, id_cliente=3, id_servicio=3, id_prestador=3,
        fecha_reserva=date(2026, 6, 14),
        fecha_servicio=date(2026, 6, 14), 
        hora_inicio=time(16, 0),            
        hora_fin=time(17, 0),              
        estado="activa", monto_reembolso=0.0, total_pagado=200.0
    )
    resultado = anticipacion(reserva_valida)
    
    if resultado:
        print("✅ Prueba Reserva Válida: Pasó con éxito (Retornó True)")
except Exception as e:
    print(f"🔴 Falló la prueba válida inesperadamente: {e}")
