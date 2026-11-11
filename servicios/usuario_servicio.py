from entidades.usuario import Usuario
from enums.rol import Rol
from excepciones.food_store_exceptions import (
    CredencialesInvalidasError,
    EntidadNoEncontradaError,
    DuplicadoError,
    OperacionNoPermitidaError
)

class UsuarioServicio:
    def __init__(self) -> None:
        self._usuarios: list[Usuario] = []

    def autenticar(self, mail: str, contrasenia: str) -> Usuario:
        mail_clean = mail.strip().lower()
        for u in self._usuarios:
            if not u.eliminado and u.mail == mail_clean:
                if u.verificar_contrasenia(contrasenia):
                    return u
        raise CredencialesInvalidasError("Mail o contraseña incorrectos")

    def crear_usuario(
        self,
        nombre: str,
        apellido: str,
        mail: str,
        celular: str,
        contrasenia: str,
        rol: Rol
    ) -> Usuario:
        mail_clean = mail.strip().lower()
        for u in self._usuarios:
            if not u.eliminado and u.mail == mail_clean:
                raise DuplicadoError(f"El mail '{mail}' ya se encuentra registrado.")
        nuevo = Usuario(
            nombre=nombre,
            apellido=apellido,
            mail=mail,
            celular=celular,
            contrasenia=contrasenia,
            rol=rol
        )
        self._usuarios.append(nuevo)
        return nuevo

    def buscar_por_id(self, usuario_id: int) -> Usuario:
        for u in self._usuarios:
            if u.id == usuario_id and not u.eliminado:
                return u
        raise EntidadNoEncontradaError(f"No se encontró el usuario con ID {usuario_id}.")

    def editar_usuario(
        self,
        usuario_id: int,
        nombre: str | None = None,
        apellido: str | None = None,
        mail: str | None = None,
        celular: str | None = None,
        rol: Rol | None = None
    ) -> Usuario:
        user = self.buscar_por_id(usuario_id)
        if mail and mail.strip():
            m_clean = mail.strip().lower()
            for u in self._usuarios:
                if not u.eliminado and u.id != usuario_id and u.mail == m_clean:
                    raise DuplicadoError(f"El mail '{mail}' ya está registrado por otro usuario.")
            user.mail = mail
        if nombre and nombre.strip():
            user.nombre = nombre
        if apellido and apellido.strip():
            user.apellido = apellido
        if celular is not None:
            user.celular = celular
        if rol is not None:
            user.rol = rol
        return user

    def eliminar_usuario(self, usuario_id: int, usuario_sesion_id: int) -> None:
        if usuario_id == usuario_sesion_id:
            raise OperacionNoPermitidaError("No puede eliminarse a sí mismo mientras tiene la sesión iniciada.")
        user = self.buscar_por_id(usuario_id)
        user.eliminado = True

    def listar_todos(self) -> list[Usuario]:
        return [u for u in self._usuarios if not u.eliminado]