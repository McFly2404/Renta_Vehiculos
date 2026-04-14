"""Value Objects del dominio de Usuarios."""
from dataclasses import dataclass


@dataclass(frozen=True)
class UsuarioData:
    """Representa los datos necesarios para registrar un nuevo usuario."""
    nombre:   str
    cedula:   str
    correo:   str
    licencia: str
