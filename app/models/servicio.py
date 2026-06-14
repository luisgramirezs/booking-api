from pydantic import BaseModel


class Servicio(BaseModel):
    id_servicio: int
    cod_servicio: str
    nombre_servicio: str
    duracion: int
    is_non_refundable: bool
    capacidad: int
    id_prestador: int
    costo_servicio: float
