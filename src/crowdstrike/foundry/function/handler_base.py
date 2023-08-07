from abc import (
    ABC,
    abstractmethod,
)
from crowdstrike.foundry.function.falconpy import falcon_client
from crowdstrike.foundry.function.model import (
    Request,
    Response,
)
from falconpy import ServiceClass
from logging import Logger
from typing import (
    Any,
    Dict,
    Type,
)


class HandlerBase(ABC):
    """
    Base class for custom SDK handlers.
    """

    _config: [Dict[str, Any], None] = None
    _logger: [Logger, None] = None

    @abstractmethod
    def handle(self, request: Request) -> Response:
        """
        Handles an inbound :class:`Request` to this function.
        :param request: Request provided to the function.
        :return: Any response the function author wishes to return to the caller.
        """
        raise NotImplementedError()

    def handler_init(self):
        """
        Called post-construction to initialize the handler's internal state.
        This method will have access to the handler's bound :class:`logging.Logger` and configuration
        via this object's `logger()` and `config()` methods.
        """
        return

    def logger(self) -> [Logger, None]:
        """
        :return: Bound :class:`logging.Logger` instance.
        """
        return self._logger

    def config(self) -> [Dict[str, Any], None]:
        """
        :return: Any bound configuration.
        """
        return self._config

    def falcon_client(self, client_class: Type) -> ServiceClass:
        """
        Returns an instance of a FalconPy client.
        :param client_class: Class which extends :class:`falconpy.ServiceClass`.
        :return: Initialized instance of the client_class.
        """
        return falcon_client(client_class)
