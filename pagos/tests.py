from django.test import SimpleTestCase

from pagos.application.services import CrearPagoService
from pagos.domain.exceptions import ReservaCanceladaError, ReservaNoEncontradaError


class FakeReserva:
    def __init__(self, estado):
        self.estado = estado


class FakeReservaRepo:
    def __init__(self, reserva=None):
        self._reserva = reserva

    def obtener_por_id(self, _reserva_id):
        return self._reserva


class FakePagoRepo:
    def obtener_por_id(self, _pago_id):
        return None

    def listar_por_reserva(self, _reserva_id):
        return []


class FakePasarela:
    def procesar(self, monto, metodo, referencia):
        return {"aprobado": True, "codigo_transaccion": "TEST1234", "mensaje": "ok"}


class CrearPagoServiceTests(SimpleTestCase):
    def test_falla_si_reserva_no_existe(self):
        service = CrearPagoService(
            reserva_repo=FakeReservaRepo(reserva=None),
            pago_repo=FakePagoRepo(),
            notificador=None,
            pasarela=FakePasarela(),
        )
        with self.assertRaises(ReservaNoEncontradaError):
            service.ejecutar(reserva_id=99, monto=1000, metodo_pago="EFECTIVO", fecha_pago="2026-05-25")

    def test_falla_si_reserva_cancelada(self):
        service = CrearPagoService(
            reserva_repo=FakeReservaRepo(reserva=FakeReserva(estado="CANCELADA")),
            pago_repo=FakePagoRepo(),
            notificador=None,
            pasarela=FakePasarela(),
        )
        with self.assertRaises(ReservaCanceladaError):
            service.ejecutar(reserva_id=1, monto=1000, metodo_pago="EFECTIVO", fecha_pago="2026-05-25")
