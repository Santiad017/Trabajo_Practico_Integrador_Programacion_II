from entidades.base import Base
from enums.rol import Rol
from excepciones.food_store_exceptions import DatoInvalidoError

class Usuario(Base):
    def __init__(self, nombre: str, apellido: str, mail: str, celular: str, contrasenia: str, rol: Rol) -> None:
        super().__init__()
        self.nombre = nombre
        self.apellido = apellido
        self.mail = mail
        self.celular = celular
        self._contrasenia = contrasenia
        self.rol = rol

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise DatoInvalidoError("El nombre no puede estar vacío.")
        self._nombre = valor.strip()

    @property
    def apellido(self) -> str:
        return self._apellido

    @apellido.setter
    def apellido(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise DatoInvalidoError("El apellido no puede estar vacío.")
        self._apellido = valor.strip()

    @property
    def mail(self) -> str:
        return self._mail

    @mail.setter
    def mail(self, valor: str) -> None:
        v = valor.strip() if valor else ""
        if not v or "@" not in v or "." not in v:
            raise DatoInvalidoError("El mail ingresado no tiene un formato válido.")
        self._mail = v.lower()

    @property
    def celular(self) -> str:
        return self._celular

    @celular.setter
    def celular(self, valor: str) -> None:
        self._celular = valor.strip() if valor else ""

    @property
    def rol(self) -> Rol:
        return self._rol

    @rol.setter
    def rol(self, valor: Rol) -> None:
        if not isinstance(valor, Rol):
            raise DatoInvalidoError("El rol debe ser un valor válido del enumerado Rol.")
        self._rol = valor

    def verificar_contrasenia(self, contrasenia: str) -> bool:
        return self._contrasenia == contrasenia

    def __str__(self) -> str:
        return f"ID: {self.id} | {self.apellido}, {self.nombre} | Email: {self.mail} | Tel: {self.celular} | Rol: {self.rol.name}"