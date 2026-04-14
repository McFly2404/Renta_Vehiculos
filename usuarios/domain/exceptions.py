"""Excepciones de dominio del contexto Usuarios."""


class UsuarioYaExisteError(Exception):
    """Cédula o correo ya registrados en el sistema."""


class UsuarioNoEncontradoError(Exception):
    """No existe un usuario con el identificador dado."""


class DatosUsuarioInvalidosError(Exception):
    """Los datos del usuario no cumplen las reglas de negocio."""
