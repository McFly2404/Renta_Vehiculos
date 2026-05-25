import os

import requests

from integraciones.domain.interfaces import IAllyServiceClient


class AllyServiceAdapter(IAllyServiceClient):
    def __init__(self, base_url: str | None = None, timeout: int = 6):
        self._base_url = base_url or os.getenv("ALLY_SERVICE_URL", "").strip()
        self._timeout = timeout

    def fetch_info(self) -> dict:
        if not self._base_url:
            return {
                "status": "not_configured",
                "message": "ALLY_SERVICE_URL is not configured.",
            }

        try:
            response = requests.get(self._base_url, timeout=self._timeout)
            response.raise_for_status()
            payload = response.json()
            return {
                "status": "ok",
                "source": self._base_url,
                "data": payload,
            }
        except requests.RequestException as exc:
            return {
                "status": "unavailable",
                "source": self._base_url,
                "error": str(exc),
            }
        except ValueError:
            return {
                "status": "invalid_payload",
                "source": self._base_url,
                "error": "The ally service did not return valid JSON.",
            }
