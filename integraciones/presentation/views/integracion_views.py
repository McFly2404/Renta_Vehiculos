from rest_framework.response import Response
from rest_framework.views import APIView

from integraciones.application.services import IntegrationsService, SystemSummaryService
from integraciones.infrastructure.adapters.ally_service_adapter import AllyServiceAdapter
from integraciones.infrastructure.adapters.open_meteo_adapter import OpenMeteoAdapter


class SystemSummaryView(APIView):
    def get(self, request):
        payload = SystemSummaryService().execute()
        return Response(payload)


class AllyServiceInfoView(APIView):
    def get(self, request):
        service = IntegrationsService(
            ally_client=AllyServiceAdapter(),
            provider=OpenMeteoAdapter(),
        )
        return Response(service.get_ally_info())


class ThirdPartyInfoView(APIView):
    def get(self, request):
        service = IntegrationsService(
            ally_client=AllyServiceAdapter(),
            provider=OpenMeteoAdapter(),
        )
        return Response(service.get_third_party_info())


class IntegrationSnapshotView(APIView):
    def get(self, request):
        service = IntegrationsService(
            ally_client=AllyServiceAdapter(),
            provider=OpenMeteoAdapter(),
        )
        return Response(service.get_combined_snapshot())
