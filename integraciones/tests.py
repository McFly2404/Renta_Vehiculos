from unittest.mock import Mock, patch

from django.test import SimpleTestCase

from integraciones.infrastructure.adapters.ally_service_adapter import AllyServiceAdapter
from integraciones.infrastructure.adapters.open_meteo_adapter import OpenMeteoAdapter


class AllyServiceAdapterTests(SimpleTestCase):
    def test_returns_not_configured_when_missing_url(self):
        adapter = AllyServiceAdapter(base_url="")
        data = adapter.fetch_info()
        self.assertEqual(data["status"], "not_configured")

    @patch("integraciones.infrastructure.adapters.ally_service_adapter.requests.get")
    def test_returns_ok_on_valid_json(self, mock_get):
        response = Mock()
        response.raise_for_status.return_value = None
        response.json.return_value = {"team": "aliado"}
        mock_get.return_value = response

        adapter = AllyServiceAdapter(base_url="http://ally.local/info")
        data = adapter.fetch_info()

        self.assertEqual(data["status"], "ok")
        self.assertEqual(data["data"]["team"], "aliado")


class OpenMeteoAdapterTests(SimpleTestCase):
    @patch("integraciones.infrastructure.adapters.open_meteo_adapter.requests.get")
    def test_parses_third_party_payload(self, mock_get):
        response = Mock()
        response.raise_for_status.return_value = None
        response.json.return_value = {
            "current": {
                "temperature_2m": 21.3,
                "relative_humidity_2m": 60,
                "wind_speed_10m": 12.5,
                "time": "2026-05-24T12:00",
            }
        }
        mock_get.return_value = response

        adapter = OpenMeteoAdapter(base_url="http://api.open-meteo.com")
        data = adapter.get_context()

        self.assertEqual(data["status"], "ok")
        self.assertEqual(data["temperature_c"], 21.3)
        self.assertEqual(data["humidity_pct"], 60)
