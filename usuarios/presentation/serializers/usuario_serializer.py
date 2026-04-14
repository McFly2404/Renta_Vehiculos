"""Serializers de presentación para Usuarios. Sin lógica de negocio."""
from rest_framework import serializers
from usuarios.models import Usuario


class UsuarioInputSerializer(serializers.Serializer):
    nombre   = serializers.CharField(max_length=100)
    cedula   = serializers.CharField(max_length=20)
    correo   = serializers.EmailField()
    licencia = serializers.CharField(max_length=50)

    def validate_nombre(self, value: str) -> str:
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Mínimo 2 caracteres.")
        return value.strip()

    def validate_cedula(self, value: str) -> str:
        cleaned = value.strip()
        if not cleaned.isalnum():
            raise serializers.ValidationError("Solo letras y números.")
        return cleaned


class UsuarioOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Usuario
        fields = ["id", "nombre", "cedula", "correo", "licencia"]
