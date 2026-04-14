from django.urls import path
from usuarios.presentation.views.usuario_views import (
    UsuarioRegistrarView,
    UsuarioListView,
    UsuarioDetailView,
)

urlpatterns = [
    path("usuarios/",          UsuarioListView.as_view(),     name="usuario-list"),
    path("usuarios/crear/",    UsuarioRegistrarView.as_view(), name="usuario-crear"),
    path("usuarios/<int:pk>/", UsuarioDetailView.as_view(),   name="usuario-detail"),
]
