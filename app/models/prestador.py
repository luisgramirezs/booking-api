from pydantic import BaseModel

class Prestador(BaseModel):
    id_prestador:int
    nombre_prestador:str
