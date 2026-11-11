from entidades.base import Base
from entidades.producto import Producto
from excepciones.food_store_exceptions import DatoInvalidoError

class DetallePedido(Base):
    def __init__(self, cantidad: int, producto: Producto) -> None:
        super().__init__()
        if producto is None or producto.eliminado:
            raise DatoInvalidoError("El producto del detalle debe ser válido.")
        self._producto = producto
        self._cantidad = 0
        self._subtotal = 0.0
        self.cantidad = cantidad

    @property
    def producto(self) -> Producto:
        return self._producto

    @property
    def cantidad(self) -> int:
        return self._cantidad

    @cantidad.setter
    def cantidad(self, valor: int) -> None:
        if valor <= 0:
            raise DatoInvalidoError("La cantidad del detalle debe ser mayor a 0.")
        self._cantidad = valor
        self._subtotal = self._cantidad * self._producto.precio

    @property
    def subtotal(self) -> float:
        return self._subtotal

    def __str__(self) -> str:
        return f"Producto: {self._producto.nombre} | Cantidad: {self._cantidad} | Subtotal: ${self._subtotal:.2f}"