"""
Capa de Aplicación — Usuarios.
SRP: una clase por caso de uso. Dependencias inyectadas por constructor (DIP).
Sin lógica en views ni en models.
"""
from usuarios.domain.repositories import IUsuarioRepository
from usuarios.domain.exceptions import UsuarioYaExisteError, UsuarioNoEncontradoError


class RegistrarUsuarioService:
    """Registra un nuevo usuario verificando unicidad de cédula y correo."""

    def __init__(self, repo: IUsuarioRepository):
        self._repo = repo

    def ejecutar(self, nombre: str, cedula: str, correo: str, licencia: str):
        if self._repo.obtener_por_cedula(cedula):
            raise UsuarioYaExisteError(f"Ya existe un usuario con la cédula '{cedula}'.")
        if self._repo.obtener_por_correo(correo):
            raise UsuarioYaExisteError(f"Ya existe un usuario con el correo '{correo}'.")
        return self._repo.crear(nombre=nombre, cedula=cedula, correo=correo, licencia=licencia)


class ObtenerUsuarioService:
    """Recupera un usuario por su ID."""

    def __init__(self, repo: IUsuarioRepository):
        self._repo = repo

    def ejecutar(self, usuario_id: int):
        usuario = self._repo.obtener_por_id(usuario_id)
        if not usuario:
            raise UsuarioNoEncontradoError(f"Usuario #{usuario_id} no encontrado.")
        return usuario


class ListarUsuariosService:
    """Devuelve todos los usuarios registrados."""

    def __init__(self, repo: IUsuarioRepository):
        self._repo = repo

    def ejecutar(self):
        return self._repo.listar()
