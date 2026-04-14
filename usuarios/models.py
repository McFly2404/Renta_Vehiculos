from django.db import models


class Usuario(models.Model):
    nombre   = models.CharField(max_length=100)
    cedula   = models.CharField(max_length=20, unique=True)
    correo   = models.EmailField(unique=True)
    licencia = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.nombre} ({self.cedula})"

    class Meta:
        verbose_name        = "Usuario"
        verbose_name_plural = "Usuarios"
