from rest_framework import serializers
from pagos.models import Pago


class PagoInputSerializer(serializers.Serializer):
    reserva_id = serializers.IntegerField()
    monto = serializers.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = serializers.ChoiceField(choices=Pago.METODO_CHOICES)
    fecha_pago = serializers.DateField()

    def validate_monto(self, value):
        if value <= 0:
            raise serializers.ValidationError("El monto debe ser mayor a 0.")
        return value


class PagoOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pago
        fields = [
            "id", "reserva", "monto", "estado_pago",
            "metodo_pago", "fecha_pago", "fecha_creacion",
        ]
