from abc import ABC, abstractmethod


class IAllyServiceClient(ABC):
    @abstractmethod
    def fetch_info(self) -> dict:
        ...


class IThirdPartyProvider(ABC):
    @abstractmethod
    def get_context(self) -> dict:
        ...
