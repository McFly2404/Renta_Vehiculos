from django.utils import timezone

from integraciones.domain.interfaces import IAllyServiceClient, IThirdPartyProvider
from pagos.models import Pago
from reservas.models import Reserva, Vehiculo
from usuarios.models import Usuario


class SystemSummaryService:
    def execute(self) -> dict:
        return {
            "timestamp": timezone.now().isoformat(),
            "usuarios": Usuario.objects.count(),
            "vehiculos": Vehiculo.objects.count(),
            "vehiculos_disponibles": Vehiculo.objects.filter(disponible=True).count(),
            "reservas": Reserva.objects.count(),
            "reservas_confirmadas": Reserva.objects.filter(estado="CONFIRMADA").count(),
            "pagos": Pago.objects.count(),
            "pagos_aprobados": Pago.objects.filter(estado_pago="APROBADO").count(),
        }


class IntegrationsService:
    def __init__(self, ally_client: IAllyServiceClient, provider: IThirdPartyProvider):
        self._ally_client = ally_client
        self._provider = provider

    def get_ally_info(self) -> dict:
        return self._ally_client.fetch_info()

    def get_third_party_info(self) -> dict:
        return self._provider.get_context()

    def get_combined_snapshot(self) -> dict:
        return {
            "timestamp": timezone.now().isoformat(),
            "ally_service": self.get_ally_info(),
            "third_party": self.get_third_party_info(),
        }
