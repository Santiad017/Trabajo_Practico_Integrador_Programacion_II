from entidades.base import Base
from entidades.categoria import Categoria
from excepciones.food_store_exceptions import DatoInvalidoError, PrecioInvalidoError

class Producto(Base):
    def __init__(
        self,
        nombre: str,
        precio: float,
        descripcion: str,
        stock: int,
        imagen: str,
        disponible: bool,
        categoria: Categoria
    ) -> None:
        # Generamos el ID especial desde la categoría ANTES de inicializar la Base
        id_generado = categoria.generar_id_producto()
        super().__init__(id_personalizado=id_generado)
        
        self.nombre = nombre
        self.precio = precio
        self.descripcion = descripcion
        self.stock = stock
        self.imagen = imagen
        self.disponible = disponible
        self.categoria = categoria

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise DatoInvalidoError("El nombre del producto no puede estar vacío.")
        self._nombre = valor.strip()

    @property
    def precio(self) -> float:
        return self._precio

    @precio.setter
    def precio(self, valor: float) -> None:
        if valor < 0:
            raise PrecioInvalidoError("El precio no puede ser negativo.")
        self._precio = float(valor)

    @property
    def descripcion(self) -> str:
        return self._descripcion

    @descripcion.setter
    def descripcion(self, valor: str) -> None:
        self._descripcion = valor.strip() if valor else ""

    @property
    def stock(self) -> int:
        return self._stock

    @stock.setter
    def stock(self, valor: int) -> None:
        if valor < 0:
            raise DatoInvalidoError("El stock no puede ser negativo.")
        self._stock = int(valor)

    @property
    def imagen(self) -> str:
        return self._imagen

    @imagen.setter
    def imagen(self, valor: str) -> None:
        self._imagen = valor.strip() if valor else ""

    @property
    def disponible(self) -> bool:
        return self._disponible

    @disponible.setter
    def disponible(self, valor: bool) -> None:
        self._disponible = bool(valor)

    @property
    def categoria(self) -> Categoria:
        return self._categoria

    @categoria.setter
    def categoria(self, valor: Categoria) -> None:
        if valor is None or valor.eliminado:
            raise DatoInvalidoError("La categoría asignada debe ser válida y no estar eliminada.")
        self._categoria = valor

    def __str__(self) -> str:
        disp_txt = "Sí" if self.disponible else "No"
        return (f"ID: {self.id} | {self.nombre} | Precio: ${self.precio:.2f} | "
                f"Stock: {self.stock} | Cat: {self.categoria.nombre} | Disponible: {disp_txt}")