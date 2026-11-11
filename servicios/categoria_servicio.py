from entidades.categoria import Categoria
from excepciones.food_store_exceptions import (
    EntidadNoEncontradaError,
    DuplicadoError,
    OperacionNoPermitidaError
)

class CategoriaServicio:
    def __init__(self) -> None:
        self._categorias: list[Categoria] = []

    def crear_categoria(self, nombre: str, descripcion: str) -> Categoria:
        nombre_clean = nombre.strip().lower()
        for cat in self._categorias:
            if not cat.eliminado and cat.nombre.lower() == nombre_clean:
                raise DuplicadoError(f"Ya existe una categoría con el nombre '{nombre}'.")
        nueva = Categoria(nombre=nombre, descripcion=descripcion)
        self._categorias.append(nueva)
        return nueva

    def buscar_por_id(self, categoria_id: int) -> Categoria:
        for cat in self._categorias:
            if cat.id == categoria_id and not cat.eliminado:
                return cat
        raise EntidadNoEncontradaError(f"No se encontró la categoría con ID {categoria_id}.")

    def editar_categoria(self, categoria_id: int, nombre: str | None = None, descripcion: str | None = None) -> Categoria:
        cat = self.buscar_por_id(categoria_id)
        if nombre and nombre.strip():
            nombre_clean = nombre.strip().lower()
            for c in self._categorias:
                if not c.eliminado and c.id != categoria_id and c.nombre.lower() == nombre_clean:
                    raise DuplicadoError(f"Ya existe otra categoría con el nombre '{nombre}'.")
            cat.nombre = nombre
        if descripcion is not None:
            cat.descripcion = descripcion
        return cat

    def eliminar_categoria(self, categoria_id: int, producto_servicio: object) -> None:
        cat = self.buscar_por_id(categoria_id)
        cant_productos = producto_servicio.contar_por_categoria(categoria_id) # type: ignore
        if cant_productos > 0:
            raise OperacionNoPermitidaError(
                f"No se puede eliminar la categoría. Tiene {cant_productos} producto(s) activo(s) asociado(s)."
            )
        cat.eliminado = True

    def listar_todas(self) -> list[Categoria]:
        return [c for c in self._categorias if not c.eliminado]