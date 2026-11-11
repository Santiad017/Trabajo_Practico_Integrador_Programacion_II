from datetime import date
from entidades.base import Base
from entidades.calculable import Calculable
from entidades.usuario import Usuario
from entidades.producto import Producto
from entidades.detalle_pedido import DetallePedido
from enums.estado import Estado
from enums.forma_pago import FormaPago
from excepciones.food_store_exceptions import DatoInvalidoError

class Pedido(Base, Calculable):
    def __init__(self, usuario: Usuario, forma_pago: FormaPago) -> None:
        super().__init__()
        if usuario is None or usuario.eliminado:
            raise DatoInvalidoError("No se puede crear un pedido sin un usuario válido.")
        self._usuario = usuario
        self._forma_pago = forma_pago
        self._fecha = date.today()
        self._estado = Estado.PENDIENTE
        self._detalles: list[DetallePedido] = []
        self._total: float = 0.0

    @property
    def usuario(self) -> Usuario:
        return self._usuario

    @property
    def forma_pago(self) -> FormaPago:
        return self._forma_pago

    @forma_pago.setter
    def forma_pago(self, valor: FormaPago) -> None:
        if not isinstance(valor, FormaPago):
            raise DatoInvalidoError("Forma de pago inválida.")
        self._forma_pago = valor

    @property
    def fecha(self) -> date:
        return self._fecha

    @property
    def estado(self) -> Estado:
        return self._estado

    @estado.setter
    def estado(self, valor: Estado) -> None:
        if not isinstance(valor, Estado):
            raise DatoInvalidoError("Estado inválido.")
        self._estado = valor

    @property
    def total(self) -> float:
        return self._total

    @property
    def detalles(self) -> tuple[DetallePedido, ...]:
        return tuple(self._detalles)

    def agregar_detalle(self, cantidad: int, producto: Producto) -> None:
        if cantidad <= 0:
            raise DatoInvalidoError("La cantidad debe ser mayor a 0.")
        if producto is None or producto.eliminado:
            raise DatoInvalidoError("El producto especificado no es válido.")

        detalle_existente = self.buscar_detalle_por_producto(producto)
        if detalle_existente:
            detalle_existente.cantidad += cantidad
        else:
            nuevo_detalle = DetallePedido(cantidad=cantidad, producto=producto)
            self._detalles.append(nuevo_detalle)
        self.calcular_total()

    def buscar_detalle_por_producto(self, producto: Producto) -> DetallePedido | None:
        for det in self._detalles:
            if not det.eliminado and det.producto.id == producto.id:
                return det
        return None

    def eliminar_detalle_por_producto(self, producto: Producto) -> None:
        det = self.buscar_detalle_por_producto(producto)
        if det:
            det.eliminado = True
            self.calcular_total()

    def calcular_total(self) -> None:
        self._total = sum(det.subtotal for det in self._detalles if not det.eliminado)

    def __str__(self) -> str:
        return (f"ID Pedido: {self.id} | Fecha: {self.fecha} | Cliente: {self.usuario.nombre} {self.usuario.apellido} | "
                f"Estado: {self.estado.name} | Pago: {self.forma_pago.name} | Total: ${self.total:.2f}")