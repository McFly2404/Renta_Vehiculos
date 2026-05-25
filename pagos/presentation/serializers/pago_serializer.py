"""Serializers de presentacion para Pagos."""
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from pagos.models import Pago


class PagoInputSerializer(serializers.Serializer):
    reserva_id = serializers.IntegerField(min_value=1)
    monto = serializers.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = serializers.ChoiceField(choices=Pago.METODO_CHOICES)
    fecha_pago = serializers.DateField()

    def validate_monto(self, value):
        if value <= 0:
            raise serializers.ValidationError(_("El monto debe ser mayor a 0."))
        return value


class PagoOutputSerializer(serializers.ModelSerializer):
    estado_pago_display = serializers.CharField(source="get_estado_pago_display", read_only=True)
    metodo_pago_display = serializers.CharField(source="get_metodo_pago_display", read_only=True)

    class Meta:
        model = Pago
        fields = [
            "id",
            "reserva",
            "monto",
            "estado_pago",
            "estado_pago_display",
            "metodo_pago",
            "metodo_pago_display",
            "fecha_pago",
            "fecha_creacion",
        ]
