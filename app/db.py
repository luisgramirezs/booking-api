import json
from app.models.cliente import Cliente
from app.models.prestador import Prestador
from app.models.reserva import Reserva
from app.models.servicio import Servicio

#Abrir y leer el seed.json
def cargar_seed(path="data/seed.json"): 
    with open (path,encoding="utf-8") as f:
        data=json.load(f)

    # Convertir cada dict en instancia de modelo

    clientes ={} 
    for c in data ["clientes"]:
        cliente_obj=Cliente(**c)
        clientes[cliente_obj.id_cliente]=cliente_obj

    prestadores ={} 
    for p in data ["prestadores"]:
        prestador_obj=Prestador(**p)
        prestadores[prestador_obj.id_prestador]=prestador_obj

    servicios ={} 
    for s in data ["servicios"]:
        servicio_obj=Servicio(**s)
        servicios[servicio_obj.id_servicio]=servicio_obj    
    
    reservas =[]
    for r in data ["reservas"]:
        reserva_obj=Reserva(**r)
        reservas.append(reserva_obj)


    # Devuelve toda la "base de datos" en memoria como un solo diccionario:
    # - clientes, prestadores, servicios: dict indexado por su ID (acceso O(1))
    # - reservas: lista (se recorre/filtra, no se accede por índice fijo)    
    
    return {
        "clientes": clientes,
        "prestadores": prestadores,
        "servicios": servicios,
        "reservas": reservas,
    }