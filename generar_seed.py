# Generar un seed para la base de datos de MongoDB con datos de ejemplo
import json # Para guardar el seed en un archivo JSON 
import random # Para generar datos aleatorios
from datetime import datetime,timedelta, time # Para generar fechas aleatorias
from faker import Faker # Para generar datos de ejemplo realistas
from pydantic import BaseModel, EmailStr # Para definir el modelo de datos, incluyendo validación de correo electrónico



# Crear una instancia de Faker para generar datos de ejemplo
fake =Faker('es_ES') # Configurar Faker para generar datos en español

# 1. Estructura de las entidades (PYDANTIC MODELS)

# Estructura de la entidad Cliente
class clienteSchema(BaseModel):
    id_cliente: int
    nombre: str
    apellido: str
    correo: EmailStr
    telefono: str
    fecha_nacimiento: str
    is_premium: bool

# Estructura de la entidad Prestador
class prestadorSchema(BaseModel):
    id_prestador: int
    nombre_prestador: str

# Estructura de la entidad Servicio
class servicioSchema(BaseModel):
    id_servicio: int
    cod_servicio: str
    nombre_servicio: str
    duracion: int
    is_non_refundable: bool
    capacidad: int
    id_prestador: int
    costo_servicio: float

# Estructura de la entidad Reserva
class reservaSchema(BaseModel):
    id_reserva: int
    id_cliente: int
    id_servicio: int
    id_prestador: int
    fecha_reserva: str
    fecha_servicio: str
    hora_inicio: str
    hora_fin: str
    estado: str
    monto_reembolso: float
    total_pagado: float

#2 Calendario valido para reservas
# No se peuden hacer reservas los dias domingos ofestivos de Colombia

#Festivos en Colombia para el año actual

festivos_2026= {
    "2026-01-01", "2026-01-12", "2026-03-23", "2026-04-02", "2026-04-03",
    "2026-05-01", "2026-05-18", "2026-06-08", "2026-06-15", "2026-06-29",
    "2026-07-13", "2026-07-20", "2026-08-07", "2026-08-17", "2026-10-12",
    "2026-11-02", "2026-11-16", "2026-12-08", "2026-12-25"
}

#Dectección de domingos y festivos:

def dia_valido(fecha: datetime):
    fecha_str=fecha.strftime('%Y-%m-%d')

    if fecha.weekday() ==6: #Dia Domingo
        return False
    if fecha_str in festivos_2026: #Día festivo Colombia
        return False
    return True


# 3. Generar datos de ejemplo para cada entidad

def generar_registros_demo(cant_clientes=10, cant_reservas=30, cant_prestadores=3, cant_servicios=5):

#Generar prestadores
    prestadores = [
        prestadorSchema(id_prestador=1, nombre_prestador= "Prestador A"),
        prestadorSchema(id_prestador=2, nombre_prestador= "Prestador B"),
        prestadorSchema(id_prestador=3, nombre_prestador= "Prestador C")
    ]

#Generar servicios
    servicios =[
        servicioSchema(id_servicio=1, cod_servicio="A01", nombre_servicio="Salón de eventos", duracion=300, costo_servicio=500.0, is_non_refundable=False, capacidad=1, id_prestador=1),
        servicioSchema(id_servicio=2, cod_servicio="B01", nombre_servicio="Catering", duracion=120, costo_servicio=200.0, is_non_refundable=True, capacidad=1, id_prestador=2),
        servicioSchema(id_servicio=3, cod_servicio="C01", nombre_servicio="Clase de Yoga personalizada", duracion=60, costo_servicio=100.0, is_non_refundable=False, capacidad=1, id_prestador=3),
        servicioSchema(id_servicio=4, cod_servicio="A01", nombre_servicio="Salón de eventos", duracion=300, costo_servicio=300.0, is_non_refundable=True, capacidad=1, id_prestador=2),
        servicioSchema(id_servicio=5, cod_servicio="D01", nombre_servicio="Cancha de fútbol", duracion=180, costo_servicio=400.0, is_non_refundable=False, capacidad=2, id_prestador=3)
    ]
#Generar clientes
    clientes=[]
    # Generar clientes con datos aleatorios utilizando Faker
    for i in range (1,cant_clientes +1): 
        fnac=fake.date_of_birth(minimum_age=18, maximum_age=70).strftime("%Y-%m-%d") # Generar fecha de nacimiento aleatoria
        clientes.append(clienteSchema(
            id_cliente=i,
            nombre=fake.first_name(),
            apellido=fake.last_name(),
            correo=fake.email(),
            telefono=fake.phone_number(),
            fecha_nacimiento=fnac,
            is_premium=random.choice([True, False])
        ))


# Generar reservas

    reservas=[]

    #Estados posibles de la reserva
    estados_reserva = ["activa", "terminada","cancelada"]

    # Generar reservas con datos aleatorios utilizando Faker 
    # y relacionando clientes, servicios y prestadores
    for i in range(1, cant_reservas + 1):
        while True:
            cliente=random.choice(clientes) # Seleccionar un cliente aleatorio
            servicio=random.choice(servicios) # Seleccionar un servicio aleatorio

            #Reglas de negocio para generar reservas coherentes:
        
            # Verificación de límite de reservas activas (Max 3)

            total_activas_cliente = 0
                
            for r_existente in reservas:
                if r_existente.id_cliente == cliente.id_cliente and r_existente.estado == "activa":
                    total_activas_cliente += 1
                
            # Si ya acumuló 3 activas en total, se bloquea la cuarta
            if total_activas_cliente >= 3:
                continue  # Rechaza el registro de prueba y genera de otro cliente.

            # No se aceptan reservas ni dimingos ni festivos de Colombia
            # Con Anticipación mínima de 2 horas
            
            while True:
                fecha_tentativa=fake.date_time_between(start_date='+2h', end_date='+30d')
                
                # Verifica si la fecha seleccionada es válida (no domingo ni festivo)
                if dia_valido(fecha_tentativa):
                    fecha_servicio=fecha_tentativa
                    break

            # Se puede reservar en el siguiente horario: de Lunes a Sábado entre 07:00 y 19:00 (hora America/Bogota)   

            #Para ello, guardamos en una variable la duración de servicio seleccionado expresado en horas

            duracion_horas = max(1, int(servicio.duracion/60))

            #El valor de la duración en horas lo restamos a la hora del cierre 19 hrs

            hora_maxima = 19- duracion_horas

            #Ahora se genera la hora de inicio aleatoria entre las 7 am y la máxima posible de acuerdo con la duración y hora de cierre
                    
            hora_inicio = datetime.combine(fecha_servicio.date(), time(random.randint(7,hora_maxima)))

            # Se calcula la hora de finalización sumando a la hora de inicio los minutos del servicio
            hora_fin = hora_inicio + timedelta(minutes=servicio.duracion)
      
            #Verificación de solapamiento de reservas:

            # Revisamos si este mismo servicio/prestador ya está ocupado en ese horario
            solapamiento = False

                
            for r_existente in reservas: 
                # Si es el mismo prestador y el mismo día, verificamos las horas
                if (r_existente.id_prestador == servicio.id_prestador and 
                    r_existente.fecha_servicio == fecha_servicio.strftime('%Y-%m-%d')):
                        
                    # Convertimos las horas de la reserva existente para comparar matemáticamente
                    existente_inicio = datetime.strptime(f"{r_existente.fecha_servicio} {r_existente.hora_inicio}", "%Y-%m-%d %H:%M")
                    existente_fin = datetime.strptime(f"{r_existente.fecha_servicio} {r_existente.hora_fin}", "%Y-%m-%d %H:%M")
                        
                    # Fórmula matemática de solapamiento:
                    # El nuevo inicio es antes del fin existente Y el nuevo fin es después del inicio existente
                    if hora_inicio < existente_fin and hora_fin > existente_inicio:
                        solapamiento = True
                        break # Se cruza, salimos del análisis para buscar otra hora

            # Si no se cruza con ninguna reserva anterior, el horario es perfecto
            if not solapamiento:
                

                # Superadas todas las validaciones se realiza el registro de la reserva

                reservas.append(reservaSchema(
                    id_reserva=i,
                    id_cliente=cliente.id_cliente,
                    id_servicio=servicio.id_servicio,
                    id_prestador=servicio.id_prestador,
                    fecha_reserva=datetime.now().strftime('%Y-%m-%d'), # <-- Directo desde el sistema
                    fecha_servicio=hora_inicio.strftime('%Y-%m-%d'),
                    hora_inicio=hora_inicio.strftime('%H:%M'),
                    hora_fin=hora_fin.strftime('%H:%M'),
                    estado=random.choice(estados_reserva),
                    monto_reembolso=0.0,
                    total_pagado=servicio.costo_servicio
                ))
                break
    return {
        "clientes": [json.loads(c.model_dump_json()) for c in clientes],
        "prestadores": [json.loads(p.model_dump_json()) for p in prestadores],
        "servicios": [json.loads(s.model_dump_json()) for s in servicios],
        "reservas": [json.loads(r.model_dump_json()) for r in reservas]
    }

# =========================================================================
# ESTE BLOQUE DEBE IR AL FINAL DE TODO, PEGADO A LA IZQUIERDA (SIN INDENTAR)
# =========================================================================
if __name__ == "__main__":
    # 1. Llamamos a la función para que genere los diccionarios en memoria
    data_final = generar_registros_demo()
    
    # 2. Guardamos los datos reales en el archivo físico
    with open("data/seed.json", "w", encoding="utf-8") as f:
        json.dump(data_final, f, ensure_ascii=False, indent=2)
        
    print("¡Archivo data/seed.json generado con éxito con todos sus registros!")

             


   