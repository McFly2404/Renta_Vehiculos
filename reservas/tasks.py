from celery import shared_task

from reservas.infrastructure.notifications.notificador_factory import NotificadorReservaFactory
from reservas.models import Reserva


@shared_task(name="reservas.notificar_reserva_creada")
def notificar_reserva_creada(reserva_id: int):
    reserva = (
        Reserva.objects.select_related("usuario", "vehiculo")
        .filter(id=reserva_id)
        .first()
    )
    if not reserva:
        return {"status": "missing", "reserva_id": reserva_id}

    notificador = NotificadorReservaFactory.crear()
    notificador.enviar_confirmacion(reserva)
    return {"status": "ok", "reserva_id": reserva_id}


@shared_task(name="reservas.generar_reporte_simple")
def generar_reporte_simple():
    total = Reserva.objects.count()
    confirmadas = Reserva.objects.filter(estado="CONFIRMADA").count()
    canceladas = Reserva.objects.filter(estado="CANCELADA").count()
    return {
        "status": "ok",
        "total_reservas": total,
        "confirmadas": confirmadas,
        "canceladas": canceladas,
    }
