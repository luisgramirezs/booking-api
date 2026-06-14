from app.db import cargar_seed

db = cargar_seed()

print("clientes:", len(db["clientes"]))
print("servicios:", len(db["servicios"]))
print("prestadores:", len(db["prestadores"]))
print("reservas:", len(db["reservas"]))
print("Cliente 10:", db["clientes"][10])