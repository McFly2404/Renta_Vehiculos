import os

import requests

from integraciones.domain.interfaces import IThirdPartyProvider


class OpenMeteoAdapter(IThirdPartyProvider):
    def __init__(self, base_url: str | None = None, timeout: int = 6):
        self._base_url = base_url or os.getenv(
            "WEATHER_API_URL",
            "https://api.open-meteo.com/v1/forecast",
        )
        self._timeout = timeout
        self._latitude = os.getenv("WEATHER_LAT", "4.7110")
        self._longitude = os.getenv("WEATHER_LON", "-74.0721")
        self._city_name = os.getenv("WEATHER_CITY", "Bogota")

    def get_context(self) -> dict:
        params = {
            "latitude": self._latitude,
            "longitude": self._longitude,
            "current": "temperature_2m,relative_humidity_2m,wind_speed_10m",
            "timezone": "auto",
        }

        try:
            response = requests.get(self._base_url, params=params, timeout=self._timeout)
            response.raise_for_status()
            payload = response.json()
            current = payload.get("current", {})
            return {
                "status": "ok",
                "source": "open-meteo",
                "city": self._city_name,
                "temperature_c": current.get("temperature_2m"),
                "humidity_pct": current.get("relative_humidity_2m"),
                "wind_kmh": current.get("wind_speed_10m"),
                "observed_at": current.get("time"),
            }
        except requests.RequestException as exc:
            return {
                "status": "unavailable",
                "source": "open-meteo",
                "error": str(exc),
            }
        except ValueError:
            return {
                "status": "invalid_payload",
                "source": "open-meteo",
                "error": "Third-party service returned invalid JSON.",
            }
