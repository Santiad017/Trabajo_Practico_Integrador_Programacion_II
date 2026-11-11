from abc import ABC, abstractmethod
from entidades.usuario import Usuario
from enums.rol import Rol
from servicios.categoria_servicio import CategoriaServicio
from servicios.producto_servicio import ProductoServicio
from servicios.usuario_servicio import UsuarioServicio
from servicios.pedido_servicio import PedidoServicio

class Menu(ABC):
    def __init__(
        self,
        usuario: Usuario,
        categoria_servicio: CategoriaServicio,
        producto_servicio: ProductoServicio,
        usuario_servicio: UsuarioServicio,
        pedido_servicio: PedidoServicio
    ) -> None:
        self._usuario = usuario
        self._categoria_servicio = categoria_servicio
        self._producto_servicio = producto_servicio
        self._usuario_servicio = usuario_servicio
        self._pedido_servicio = pedido_servicio

    @abstractmethod
    def mostrar(self) -> bool:
        """Muestra el menú. Retorna True para cerrar sesión, False para salir de la aplicación."""
        pass

def crear_menu(
    usuario: Usuario,
    categoria_servicio: CategoriaServicio,
    producto_servicio: ProductoServicio,
    usuario_servicio: UsuarioServicio,
    pedido_servicio: PedidoServicio
) -> Menu:
    from consola.menu_administrador import MenuAdministrador
    from consola.menu_cliente import MenuCliente

    if usuario.rol == Rol.ADMIN:
        return MenuAdministrador(usuario, categoria_servicio, producto_servicio, usuario_servicio, pedido_servicio)
    return MenuCliente(usuario, categoria_servicio, producto_servicio, usuario_servicio, pedido_servicio)