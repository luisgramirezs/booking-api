from pydantic import BaseModel , EmailStr
from datetime import date


class Cliente(BaseModel):
    id_cliente: int
    nombre: str
    apellido: str
    correo: EmailStr
    telefono: str
    fecha_nacimiento: date
    is_premium: bool