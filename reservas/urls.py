from django.urls import path
from reservas.presentation.views.reserva_views import (
    ReservaCreateView,
    ReservaListView,
    ReservaDetailView,
    ReservaCancelarView,
    VehiculoListView,
)

urlpatterns = [
    path("reservas/",                   ReservaListView.as_view(),     name="reserva-list"),
    path("reservas/crear/",             ReservaCreateView.as_view(),   name="reserva-crear"),
    path("reservas/<int:pk>/",          ReservaDetailView.as_view(),   name="reserva-detail"),
    path("reservas/<int:pk>/cancelar/", ReservaCancelarView.as_view(), name="reserva-cancelar"),
    path("vehiculos/",                  VehiculoListView.as_view(),    name="vehiculo-list"),
]
