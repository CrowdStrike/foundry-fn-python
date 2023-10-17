from crowdstrike.foundry.function.model import FDKException, Request, Response
from dataclasses import dataclass
from http.client import BAD_REQUEST, METHOD_NOT_ALLOWED, NOT_FOUND, SERVICE_UNAVAILABLE
from typing import Callable


@dataclass
class Route:
    func: Callable
    method: str
    path: str


class Router:
    """
    Serves to route function requests to the appropriate handler functions.
    """

    def __init__(self, logger, config):
        self._config = config
        self._logger = logger
        self._routes = {}

    def route(self, req: Request) -> Response:
        """
        Given the method and path of a :class:`Request`, invokes the corresponding handler if one exists.
        :param req: :class:`Request` presented to the function.
        :return: :class:`Response` from the handler.
        :raise FDKException: Path-method mismatch.
        """
        if type(req.url) is not str:
            raise FDKException(code=BAD_REQUEST,
                               message="Unsupported URL format, expects string: {}".format(req.url))
        if type(req.method) is not str:
            raise FDKException(code=BAD_REQUEST,
                               message="Unsupported method format, expects string: {}".format(req.method))

        methods_for_url = self._routes.get(req.url, None)
        if methods_for_url is None:
            raise FDKException(code=NOT_FOUND, message="Not Found: {}".format(req.url))

        req_method = req.method.strip().upper()
        r = methods_for_url.get(req_method, None)
        if r is None:
            raise FDKException(code=METHOD_NOT_ALLOWED, message="Method Not Allowed: {}".format(req_method))

        return r.func(req, self._logger, self._config)

    def register(self, r: Route):
        """
        Registers a :class:`Route` with this instance.
        :param r: :class:`Route` to register.
        """
        r.method = r.method.upper().strip()
        if r.method not in {'DELETE', 'GET', 'PATCH', 'POST', 'PUT', }:
            raise FDKException(code=SERVICE_UNAVAILABLE, message='Unsupported method: ' + r.method)

        methods_for_path = self._routes.get(r.path, {})
        if r.method in methods_for_path:
            raise FDKException(code=SERVICE_UNAVAILABLE,
                               message='Duplicate method path combination: {} {}'.format(r.method, r.path))

        methods_for_path[r.method] = r
        self._routes[r.path] = methods_for_path
