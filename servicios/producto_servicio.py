from entidades.producto import Producto
from entidades.categoria import Categoria
from excepciones.food_store_exceptions import EntidadNoEncontradaError

class ProductoServicio:
    def __init__(self) -> None:
        self._productos: list[Producto] = []

    def crear_producto(
        self,
        nombre: str,
        precio: float,
        descripcion: str,
        stock: int,
        imagen: str,
        disponible: bool,
        categoria: Categoria
    ) -> Producto:
        nuevo = Producto(
            nombre=nombre,
            precio=precio,
            descripcion=descripcion,
            stock=stock,
            imagen=imagen,
            disponible=disponible,
            categoria=categoria
        )
        self._productos.append(nuevo)
        return nuevo

    def buscar_por_id(self, producto_id: int) -> Producto:
        for p in self._productos:
            if p.id == producto_id and not p.eliminado:
                return p
        raise EntidadNoEncontradaError(f"No se encontró el producto con ID {producto_id}.")

    def editar_producto(
        self,
        producto_id: int,
        nombre: str | None = None,
        precio: float | None = None,
        descripcion: str | None = None,
        stock: int | None = None,
        imagen: str | None = None,
        disponible: bool | None = None,
        categoria: Categoria | None = None
    ) -> Producto:
        prod = self.buscar_por_id(producto_id)
        if nombre is not None and nombre.strip():
            prod.nombre = nombre
        if precio is not None:
            prod.precio = precio
        if descripcion is not None:
            prod.descripcion = descripcion
        if stock is not None:
            prod.stock = stock
        if imagen is not None:
            prod.imagen = imagen
        if disponible is not None:
            prod.disponible = disponible
        if categoria is not None:
            prod.categoria = categoria
        return prod

    def eliminar_producto(self, producto_id: int) -> None:
        prod = self.buscar_por_id(producto_id)
        prod.eliminado = True

    def listar_todos(self) -> list[Producto]:
        return [p for p in self._productos if not p.eliminado]

    def listar_disponibles_con_stock(self) -> list[Producto]:
        return [p for p in self._productos if not p.eliminado and p.disponible and p.stock > 0]

    def contar_por_categoria(self, categoria_id: int) -> int:
        return len([p for p in self._productos if not p.eliminado and p.categoria.id == categoria_id])