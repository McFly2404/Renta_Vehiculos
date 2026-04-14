"""
Vistas DRF para Pagos.
Patrón: serializer → service → Response. Sin lógica de negocio.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from pagos.presentation.serializers.pago_serializer import PagoInputSerializer, PagoOutputSerializer
from pagos.application.services import CrearPagoService, ObtenerPagoService
from pagos.infrastructure.repositories.django_pago_repository import DjangoPagoRepository
from pagos.infrastructure.notifications.notificador_factory import NotificadorPagoFactory
from pagos.infrastructure.gateways.pasarela_factory import PasarelaFactory
from reservas.infrastructure.repositories.django_reserva_repository import DjangoReservaRepository
from pagos.domain.exceptions import (
    ReservaNoEncontradaError,
    PagoYaRegistradoError,
    ReservaCanceladaError,
    PagoNoEncontradoError,
)


class PagoCreateView(APIView):
    """POST /api/pagos/ — Registra un pago para una reserva."""

    def post(self, request):
        serializer = PagoInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        service = CrearPagoService(
            reserva_repo = DjangoReservaRepository(),
            pago_repo    = DjangoPagoRepository(),
            notificador  = NotificadorPagoFactory.crear(),
            pasarela     = PasarelaFactory.crear(),
        )
        try:
            pago = service.ejecutar(**serializer.validated_data)
        except ReservaNoEncontradaError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except (PagoYaRegistradoError, ReservaCanceladaError) as e:
            return Response({"error": str(e)}, status=status.HTTP_409_CONFLICT)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(PagoOutputSerializer(pago).data, status=status.HTTP_201_CREATED)


class PagoDetailView(APIView):
    """GET /api/pagos/<id>/ — Detalle de un pago."""

    def get(self, request, pk):
        service = ObtenerPagoService(pago_repo=DjangoPagoRepository())
        try:
            pago = service.ejecutar(pk)
        except PagoNoEncontradoError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        return Response(PagoOutputSerializer(pago).data)
