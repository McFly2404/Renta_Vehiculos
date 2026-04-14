"""
Implementación concreta del repositorio de Usuarios usando Django ORM.
Puede ser reemplazada por cualquier otra implementación sin tocar el dominio (DIP).
"""
from typing import Optional
from usuarios.models import Usuario
from usuarios.domain.repositories import IUsuarioRepository


class DjangoUsuarioRepository(IUsuarioRepository):

    def obtener_por_id(self, usuario_id: int) -> Optional[Usuario]:
        try:
            return Usuario.objects.get(id=usuario_id)
        except Usuario.DoesNotExist:
            return None

    def obtener_por_cedula(self, cedula: str) -> Optional[Usuario]:
        return Usuario.objects.filter(cedula=cedula).first()

    def obtener_por_correo(self, correo: str) -> Optional[Usuario]:
        return Usuario.objects.filter(correo=correo).first()

    def crear(self, nombre: str, cedula: str, correo: str, licencia: str) -> Usuario:
        return Usuario.objects.create(
            nombre=nombre, cedula=cedula, correo=correo, licencia=licencia
        )

    def listar(self):
        return Usuario.objects.all().order_by("nombre")
