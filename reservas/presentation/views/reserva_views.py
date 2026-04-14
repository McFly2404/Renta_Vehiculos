"""
Vistas DRF para Reservas y Vehículos.
Patrón: serializer → service → Response. Sin lógica de negocio.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from reservas.presentation.serializers.reserva_serializer import (
    ReservaInputSerializer,
    ReservaOutputSerializer,
    VehiculoOutputSerializer,
)
from reservas.application.services import (
    CrearReservaService,
    CancelarReservaService,
    ObtenerReservaService,
    ListarReservasService,
    ListarVehiculosService,
)
from reservas.infrastructure.repositories.django_reserva_repository import (
    DjangoVehiculoRepository,
    DjangoReservaRepository,
)
from reservas.infrastructure.notifications.notificador_factory import NotificadorReservaFactory
from usuarios.infrastructure.repositories.django_usuario_repository import DjangoUsuarioRepository
from reservas.domain.exceptions import (
    VehiculoNoEncontradoError,
    VehiculoNoDisponibleError,
    ReservaNoEncontradaError,
    ReservaYaCanceladaError,
    FechasInvalidasError,
)
from usuarios.domain.exceptions import UsuarioNoEncontradoError


class ReservaCreateView(APIView):
    """POST /api/reservas/crear/ — Crea una reserva usando la placa del vehículo."""

    def post(self, request):
        serializer = ReservaInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        service = CrearReservaService(
            vehiculo_repo = DjangoVehiculoRepository(),
            usuario_repo  = DjangoUsuarioRepository(),
            reserva_repo  = DjangoReservaRepository(),
            notificador   = NotificadorReservaFactory.crear(),
        )
        try:
            reserva = service.ejecutar(**serializer.validated_data)
        except (UsuarioNoEncontradoError, VehiculoNoEncontradoError) as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except VehiculoNoDisponibleError as e:
            return Response({"error": str(e)}, status=status.HTTP_409_CONFLICT)
        except (ValueError, FechasInvalidasError) as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(ReservaOutputSerializer(reserva).data, status=status.HTTP_201_CREATED)


class ReservaListView(APIView):
    """GET /api/reservas/ — Lista todas las reservas."""

    def get(self, request):
        service  = ListarReservasService(reserva_repo=DjangoReservaRepository())
        reservas = service.ejecutar()
        return Response(ReservaOutputSerializer(reservas, many=True).data)


class ReservaDetailView(APIView):
    """GET /api/reservas/<id>/ — Detalle de una reserva."""

    def get(self, request, pk):
        service = ObtenerReservaService(reserva_repo=DjangoReservaRepository())
        try:
            reserva = service.ejecutar(pk)
        except ReservaNoEncontradaError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        return Response(ReservaOutputSerializer(reserva).data)


class ReservaCancelarView(APIView):
    """POST /api/reservas/<id>/cancelar/ — Cancela una reserva."""

    def post(self, request, pk):
        service = CancelarReservaService(
            reserva_repo  = DjangoReservaRepository(),
            vehiculo_repo = DjangoVehiculoRepository(),
        )
        try:
            reserva = service.ejecutar(pk)
        except ReservaNoEncontradaError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except ReservaYaCanceladaError as e:
            return Response({"error": str(e)}, status=status.HTTP_409_CONFLICT)
        return Response(ReservaOutputSerializer(reserva).data)


class VehiculoListView(APIView):
    """GET /api/vehiculos/ — Lista vehículos; ?disponible=true filtra disponibles."""

    def get(self, request):
        solo_disponibles = request.query_params.get("disponible", "").lower() == "true"
        service   = ListarVehiculosService(vehiculo_repo=DjangoVehiculoRepository())
        vehiculos = service.ejecutar(solo_disponibles=solo_disponibles)
        return Response(VehiculoOutputSerializer(vehiculos, many=True).data)
