from celery import shared_task

from pagos.infrastructure.notifications.notificador_factory import NotificadorPagoFactory
from pagos.models import Pago


@shared_task(name="pagos.notificar_pago_confirmado")
def notificar_pago_confirmado(pago_id: int):
    pago = Pago.objects.select_related("reserva").filter(id=pago_id).first()
    if not pago:
        return {"status": "missing", "pago_id": pago_id}

    notificador = NotificadorPagoFactory.crear()
    notificador.enviar_confirmacion(pago)
    return {"status": "ok", "pago_id": pago_id}
