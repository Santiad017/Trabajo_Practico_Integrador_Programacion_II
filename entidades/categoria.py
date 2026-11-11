from entidades.base import Base
from excepciones.food_store_exceptions import DatoInvalidoError

class Categoria(Base):
    def __init__(self, nombre: str, descripcion: str) -> None:
        super().__init__()
        self.nombre = nombre
        self.descripcion = descripcion
        self._contador_productos: int = 0  # Lleva la cuenta de cuántos productos tiene esta categoría

    def generar_id_producto(self) -> int:
        """Genera un ID de 3 dígitos empezando por el ID de la categoría (ej: Cat 1 -> 101, 102)."""
        self._contador_productos += 1
        return (self.id * 100) + self._contador_productos

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise DatoInvalidoError("El nombre de la categoría no puede estar vacío.")
        self._nombre = valor.strip()

    @property
    def descripcion(self) -> str:
        return self._descripcion

    @descripcion.setter
    def descripcion(self, valor: str) -> None:
        self._descripcion = valor.strip() if valor else ""

    def __str__(self) -> str:
        return f"ID: {self.id} | Categoría: {self.nombre} | Desc: {self.descripcion}"