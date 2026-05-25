from django.urls import path

from integraciones.presentation.views.integracion_views import (
    AllyServiceInfoView,
    IntegrationSnapshotView,
    SystemSummaryView,
    ThirdPartyInfoView,
)

urlpatterns = [
    path("integraciones/resumen/", SystemSummaryView.as_view(), name="integraciones-resumen"),
    path("integraciones/aliado/", AllyServiceInfoView.as_view(), name="integraciones-aliado"),
    path("integraciones/tercero/", ThirdPartyInfoView.as_view(), name="integraciones-tercero"),
    path("integraciones/snapshot/", IntegrationSnapshotView.as_view(), name="integraciones-snapshot"),
]
