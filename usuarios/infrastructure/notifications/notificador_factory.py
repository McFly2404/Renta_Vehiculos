"""
Factory de notificadores para Usuarios (Factory Method — GoF).
Decide qué canal usar según el entorno, sin que el Service lo sepa.
"""
import os


class _NotificadorConsola:
    def enviar_bienvenida(self, usuario) -> None:
        print(f"[DEV]  Bienvenido, {usuario.nombre}! Cuenta creada (ID {usuario.id}).")


class _NotificadorEmail:
    def enviar_bienvenida(self, usuario) -> None:
        # En producción: integrar con SMTP / SendGrid / SES, etc.
        print(f"[PROD] Email de bienvenida enviado a {usuario.correo}.")


class NotificadorUsuarioFactory:

    @staticmethod
    def crear():
        return _NotificadorEmail() if os.getenv("ENV") == "PROD" else _NotificadorConsola()
