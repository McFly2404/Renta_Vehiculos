"""
Capa de Aplicación — Reservas.
SRP: una clase por caso de uso. DIP: dependencias inyectadas por constructor.
Prohibido: lógica de negocio en views o models.
"""
from reservas.domain.repositories import IVehiculoRepository, IReservaRepository
from reservas.domain.reserva_builder import ReservaBuilder
from reservas.domain.exceptions import (
    VehiculoNoEncontradoError,
    VehiculoNoDisponibleError,
    ReservaNoEncontradaError,
    ReservaYaCanceladaError,
)
from usuarios.domain.repositories import IUsuarioRepository
from usuarios.domain.exceptions import UsuarioNoEncontradoError


class CrearReservaService:
    """Orquesta la creación de una reserva. Busca el vehículo por placa."""

    def __init__(
        self,
        vehiculo_repo: IVehiculoRepository,
        usuario_repo:  IUsuarioRepository,
        reserva_repo:  IReservaRepository,
        notificador,
    ):
        self._vehiculo_repo = vehiculo_repo
        self._usuario_repo  = usuario_repo
        self._reserva_repo  = reserva_repo
        self._notificador   = notificador

    def ejecutar(self, usuario_id: int, placa_vehiculo: str, fecha_inicio, fecha_fin):
        usuario = self._usuario_repo.obtener_por_id(usuario_id)
        if not usuario:
            raise UsuarioNoEncontradoError(f"Usuario #{usuario_id} no encontrado.")

        vehiculo = self._vehiculo_repo.obtener_por_placa(placa_vehiculo)
        if not vehiculo:
            raise VehiculoNoEncontradoError(
                f"Vehículo con placa '{placa_vehiculo}' no encontrado."
            )
        if not vehiculo.disponible:
            raise VehiculoNoDisponibleError(
                f"El vehículo {vehiculo.placa} no está disponible."
            )

        reserva = (
            ReservaBuilder()
            .para_usuario(usuario)
            .para_vehiculo(vehiculo)
            .en_fechas(fecha_inicio, fecha_fin)
            .build()
        )

        self._vehiculo_repo.marcar_no_disponible(vehiculo)
        self._notificador.enviar_confirmacion(reserva)
        return reserva


class CancelarReservaService:
    """Cancela una reserva y libera el vehículo."""

    def __init__(
        self,
        reserva_repo:  IReservaRepository,
        vehiculo_repo: IVehiculoRepository,
    ):
        self._reserva_repo  = reserva_repo
        self._vehiculo_repo = vehiculo_repo

    def ejecutar(self, reserva_id: int):
        reserva = self._reserva_repo.obtener_por_id(reserva_id)
        if not reserva:
            raise ReservaNoEncontradaError(f"Reserva #{reserva_id} no encontrada.")
        if reserva.estado == "CANCELADA":
            raise ReservaYaCanceladaError("La reserva ya se encuentra cancelada.")

        reserva = self._reserva_repo.cancelar(reserva)
        self._vehiculo_repo.marcar_disponible(reserva.vehiculo)
        return reserva


class ObtenerReservaService:
    """Recupera una reserva por su ID."""

    def __init__(self, reserva_repo: IReservaRepository):
        self._reserva_repo = reserva_repo

    def ejecutar(self, reserva_id: int):
        reserva = self._reserva_repo.obtener_por_id(reserva_id)
        if not reserva:
            raise ReservaNoEncontradaError(f"Reserva #{reserva_id} no encontrada.")
        return reserva


class ListarReservasService:
    """Lista todas las reservas del sistema."""

    def __init__(self, reserva_repo: IReservaRepository):
        self._reserva_repo = reserva_repo

    def ejecutar(self):
        return self._reserva_repo.listar_todas()


class ListarVehiculosService:
    """Lista vehículos con filtro opcional de disponibilidad."""

    def __init__(self, vehiculo_repo: IVehiculoRepository):
        self._vehiculo_repo = vehiculo_repo

    def ejecutar(self, solo_disponibles: bool = False):
        if solo_disponibles:
            return self._vehiculo_repo.listar_disponibles()
        return self._vehiculo_repo.listar_todos()
