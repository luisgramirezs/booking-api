from pydantic import BaseModel, model_validator
from datetime import date, time


class Reserva(BaseModel):
    id_reserva: int
    id_cliente: int
    id_servicio: int
    id_prestador: int
    fecha_reserva: date
    fecha_servicio: date
    hora_inicio: time
    hora_fin: time
    estado: str
    monto_reembolso: float
    total_pagado: float

    @model_validator(mode="after")
    def hora_fin_despues_de_inicio(self):
        if self.hora_fin <= self.hora_inicio:
            raise ValueError("hora_fin debe ser posterior a hora_inicio")
        return self
