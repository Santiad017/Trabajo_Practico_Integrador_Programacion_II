from enum import Enum, auto

class Estado(Enum):
    PENDIENTE = auto()
    CONFIRMADO = auto()
    TERMINADO = auto()
    CANCELADO = auto()