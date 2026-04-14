"""Serializers de presentación para Reservas. Sin lógica de negocio."""
from datetime import date
from rest_framework import serializers
from reservas.models import Reserva, Vehiculo, Sucursal
from usuarios.presentation.serializers.usuario_serializer import UsuarioOutputSerializer


class SucursalOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Sucursal
        fields = ["id", "nombre", "ciudad"]


class VehiculoOutputSerializer(serializers.ModelSerializer):
    sucursal = SucursalOutputSerializer(read_only=True)

    class Meta:
        model  = Vehiculo
        fields = [
            "id", "placa", "modelo", "categoria",
            "capacidad", "color", "tarifa_diaria", "disponible", "sucursal",
        ]


class ReservaInputSerializer(serializers.Serializer):
    usuario_id     = serializers.IntegerField(min_value=1)
    placa_vehiculo = serializers.CharField(max_length=20)
    fecha_inicio   = serializers.DateField()
    fecha_fin      = serializers.DateField()

    def validate(self, data):
        if data["fecha_inicio"] >= data["fecha_fin"]:
            raise serializers.ValidationError(
                "La fecha de inicio debe ser anterior a la fecha de fin."
            )
        if data["fecha_inicio"] < date.today():
            raise serializers.ValidationError(
                "La fecha de inicio no puede ser en el pasado."
            )
        return data


class ReservaOutputSerializer(serializers.ModelSerializer):
    usuario  = UsuarioOutputSerializer(read_only=True)
    vehiculo = VehiculoOutputSerializer(read_only=True)

    class Meta:
        model  = Reserva
        fields = [
            "id", "usuario", "vehiculo",
            "fecha_inicio", "fecha_fin", "estado", "fecha_creacion",
        ]
