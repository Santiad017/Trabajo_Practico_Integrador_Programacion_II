from enum import Enum, auto

class FormaPago(Enum):
    TARJETA = auto()
    TRANSFERENCIA = auto()
    EFECTIVO = auto()