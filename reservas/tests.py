from django.test import SimpleTestCase

from reservas.application.services import ListarVehiculosService


class FakeVehiculoRepo:
    def listar_disponibles(self):
        return ["disponible"]

    def listar_no_disponibles(self):
        return ["ocupado"]

    def listar_todos(self):
        return ["todos"]


class ListarVehiculosServiceTests(SimpleTestCase):
    def setUp(self):
        self.service = ListarVehiculosService(vehiculo_repo=FakeVehiculoRepo())

    def test_filtra_disponibles(self):
        result = self.service.ejecutar(disponible=True)
        self.assertEqual(result, ["disponible"])

    def test_filtra_no_disponibles(self):
        result = self.service.ejecutar(disponible=False)
        self.assertEqual(result, ["ocupado"])

    def test_sin_filtro_retorna_todos(self):
        result = self.service.ejecutar(disponible=None)
        self.assertEqual(result, ["todos"])
