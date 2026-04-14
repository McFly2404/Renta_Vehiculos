"""
Vistas DRF para Usuarios.
Patrón: serializer → service → Response. Sin lógica de negocio.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from usuarios.presentation.serializers.usuario_serializer import (
    UsuarioInputSerializer,
    UsuarioOutputSerializer,
)
from usuarios.application.services import (
    RegistrarUsuarioService,
    ObtenerUsuarioService,
    ListarUsuariosService,
)
from usuarios.infrastructure.repositories.django_usuario_repository import DjangoUsuarioRepository
from usuarios.domain.exceptions import UsuarioYaExisteError, UsuarioNoEncontradoError


class UsuarioRegistrarView(APIView):
    """POST /api/usuarios/crear/ — Registra un nuevo usuario."""

    def post(self, request):
        serializer = UsuarioInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        service = RegistrarUsuarioService(repo=DjangoUsuarioRepository())
        try:
            usuario = service.ejecutar(**serializer.validated_data)
        except UsuarioYaExisteError as e:
            return Response({"error": str(e)}, status=status.HTTP_409_CONFLICT)

        return Response(UsuarioOutputSerializer(usuario).data, status=status.HTTP_201_CREATED)


class UsuarioListView(APIView):
    """GET /api/usuarios/ — Lista todos los usuarios."""

    def get(self, request):
        service  = ListarUsuariosService(repo=DjangoUsuarioRepository())
        usuarios = service.ejecutar()
        return Response(UsuarioOutputSerializer(usuarios, many=True).data)


class UsuarioDetailView(APIView):
    """GET /api/usuarios/<id>/ — Detalle de un usuario."""

    def get(self, request, pk):
        service = ObtenerUsuarioService(repo=DjangoUsuarioRepository())
        try:
            usuario = service.ejecutar(pk)
        except UsuarioNoEncontradoError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        return Response(UsuarioOutputSerializer(usuario).data)
