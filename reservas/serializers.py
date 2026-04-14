from rest_framework import serializers
from reservas.models import Usuario, Sucursal, Vehiculo, Reserva, ContratoAlquiler


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ["id", "nombre", "cedula", "correo", "licencia"]


class SucursalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sucursal
        fields = ["id", "nombre", "direccion", "telefono", "ciudad"]


class VehiculoSerializer(serializers.ModelSerializer):
    sucursal_nombre = serializers.CharField(source="sucursal.nombre", read_only=True)

    class Meta:
        model = Vehiculo
        fields = [
            "id", "placa", "modelo", "categoria", "capacidad",
            "color", "tarifa_diaria", "disponible", "sucursal", "sucursal_nombre",
        ]


class ReservaInputSerializer(serializers.Serializer):
    usuario_id = serializers.IntegerField()
    vehiculo_id = serializers.IntegerField()
    fecha_inicio = serializers.DateField()
    fecha_fin = serializers.DateField()

    def validate(self, data):
        from datetime import date
        if data["fecha_inicio"] >= data["fecha_fin"]:
            raise serializers.ValidationError(
                "La fecha de inicio debe ser anterior a la fecha fin."
            )
        if data["fecha_inicio"] < date.today():
            raise serializers.ValidationError(
                "La fecha de inicio no puede ser en el pasado."
            )
        return data


class ReservaOutputSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(read_only=True)
    vehiculo = VehiculoSerializer(read_only=True)

    class Meta:
        model = Reserva
        fields = [
            "id", "usuario", "vehiculo",
            "fecha_inicio", "fecha_fin", "estado", "fecha_creacion",
        ]


class ContratoAlquilerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContratoAlquiler
        fields = ["id", "usuario", "vehiculo", "pago", "fecha_inicio", "fecha_fin", "fecha_creacion"]
