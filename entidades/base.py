from abc import ABC
from datetime import datetime

class Base(ABC):
    _contador_id: int = 0

    def __init__(self) -> None:
        Base._contador_id += 1
        self._id: int = Base._contador_id
        self._eliminado: bool = False
        self._creado_en: datetime = datetime.now()

    @property
    def id(self) -> int:
        return self._id

    @property
    def eliminado(self) -> bool:
        return self._eliminado

    @eliminado.setter
    def eliminado(self, valor: bool) -> None:
        self._eliminado = bool(valor)

    @property
    def creado_en(self) -> datetime:
        return self._creado_en

    def __eq__(self, otro: object) -> bool:
        if not isinstance(otro, Base):
            return False
        return self.id == otro.id and type(self) is type(otro)