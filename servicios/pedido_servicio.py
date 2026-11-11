from entidades.pedido import Pedido
from entidades.usuario import Usuario
from entidades.producto import Producto
from enums.estado import Estado
from enums.forma_pago import FormaPago
from excepciones.food_store_exceptions import (
    EntidadNoEncontradaError,
    StockInsuficienteError,
    OperacionNoPermitidaError,
    DatoInvalidoError
)

class PedidoServicio:
    def __init__(self) -> None:
        self._pedidos: list[Pedido] = []

    def crear_pedido(self, usuario: Usuario, forma_pago: FormaPago, items: list[tuple[Producto, int]]) -> Pedido:
        if not items:
            raise DatoInvalidoError("El pedido debe tener al menos un producto.")
        
        # Validar stock total requerido antes de modificar datos
        recaudo_stock: dict[int, int] = {}
        for prod, cant in items:
            if cant <= 0:
                raise DatoInvalidoError(f"La cantidad para '{prod.nombre}' debe ser mayor a 0.")
            recaudo_stock[prod.id] = recaudo_stock.get(prod.id, 0) + cant

        for prod, cant in items:
            if recaudo_stock[prod.id] > prod.stock:
                raise StockInsuficienteError(
                    f"Stock insuficiente para '{prod.nombre}'. Requerido: {recaudo_stock[prod.id]}, Disponible: {prod.stock}"
                )

        pedido = Pedido(usuario=usuario, forma_pago=forma_pago)

        for prod, cant in items:
            pedido.agregar_detalle(cantidad=cant, producto=prod)
            prod.stock -= cant

        self._pedidos.append(pedido)
        return pedido

    def buscar_por_id(self, pedido_id: int) -> Pedido:
        for p in self._pedidos:
            if p.id == pedido_id and not p.eliminado:
                return p
        raise EntidadNoEncontradaError(f"No se encontró el pedido con ID {pedido_id}.")

    def cambiar_estado(self, pedido_id: int, nuevo_estado: Estado) -> Pedido:
        pedido = self.buscar_por_id(pedido_id)
        actual = pedido.estado

        if actual in (Estado.TERMINADO, Estado.CANCELADO):
            raise OperacionNoPermitidaError(f"No se puede modificar un pedido en estado {actual.name}.")

        transiciones_validas = {
            Estado.PENDIENTE: [Estado.CONFIRMADO, Estado.CANCELADO],
            Estado.CONFIRMADO: [Estado.TERMINADO, Estado.CANCELADO]
        }

        if nuevo_estado not in transiciones_validas.get(actual, []):
            raise OperacionNoPermitidaError(
                f"Transición de estado inválida: de {actual.name} a {nuevo_estado.name}."
            )

        if nuevo_estado == Estado.CANCELADO:
            for det in pedido.detalles:
                if not det.eliminado:
                    det.producto.stock += det.cantidad

        pedido.estado = nuevo_estado
        return pedido

    def eliminar_pedido(self, pedido_id: int) -> None:
        pedido = self.buscar_por_id(pedido_id)
        if pedido.estado not in (Estado.TERMINADO, Estado.CANCELADO):
            for det in pedido.detalles:
                if not det.eliminado:
                    det.producto.stock += det.cantidad
        
        pedido.eliminado = True
        for det in pedido.detalles:
            det.eliminado = True

    def listar_todos(self) -> list[Pedido]:
        return [p for p in self._pedidos if not p.eliminado]

    def listar_por_usuario(self, usuario_id: int) -> list[Pedido]:
        return [p for p in self._pedidos if not p.eliminado and p.usuario.id == usuario_id]