from django.urls import path
from pagos.presentation.views.pago_views import PagoCreateView, PagoDetailView

urlpatterns = [
    path("pagos/",          PagoCreateView.as_view(),  name="pago-crear"),
    path("pagos/<int:pk>/", PagoDetailView.as_view(),  name="pago-detail"),
]
