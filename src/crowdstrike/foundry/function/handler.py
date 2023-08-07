import json
import signal
import sys
from abc import ABCMeta
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler
from logging import Logger
from crowdstrike.foundry.function.config_loader import load_config
from crowdstrike.foundry.function.handler_base import HandlerBase
from crowdstrike.foundry.function.logger import new_logger
from crowdstrike.foundry.function.model import (
    Request,
    Response,
    ctx_request,
)
from typing import (
    Any,
    Dict,
    Type,
)


class Handler(BaseHTTPRequestHandler):
    """
    CrowdStrike SDK handler driver.
    """
    config: [Dict[str, Any], None] = None
    handler: [HandlerBase, None] = None
    logger: [Logger, None] = None
    bootstrapped: bool = False
    write_delegate = None

    @staticmethod
    def bind_handler(handler_class: Type):
        """
        Constructs and binds a new instance of :class:`HandlerBase` from the provided class.
        :param handler_class: Class from which to construct the :class:`HandlerBase`.
        This must extend :class:`HandlerBase`.
        """
        Handler.handler = resolve_user_handler(handler_class)

    @staticmethod
    def load():
        """
        Loads a logger and configuration.
        :raises AssertionError: Successfully read the configuration file but the file was considered empty.
        """
        log = new_logger()
        Handler.logger = log

        signal.signal(signal.SIGINT, shutdown)
        signal.signal(signal.SIGTERM, shutdown)

        Handler.config = load_config(log)

    def do_DELETE(self):
        """
        Executes on HTTP DELETE.
        """
        self._exec_request()

    def do_GET(self):
        """
        Executes on HTTP GET.
        """
        self._exec_request()

    def do_HEAD(self):
        """
        Executes on HTTP HEAD.
        """
        self._exec_request()

    def do_OPTIONS(self):
        """
        Executes on HTTP OPTIONS.
        """
        self._exec_request()

    def do_PATCH(self):
        """
        Executes on HTTP PATCH.
        """
        self._exec_request()

    def do_POST(self):
        """
        Executes on HTTP POST.
        """
        self._exec_request()

    def do_PUT(self):
        """
        Executes on HTTP PUT.
        """
        self._exec_request()

    def _exec_request(self):
        Handler.logger.info('received request')
        req = self._read_request()
        ctx_request.set(req)
        resp = Handler.handler.handle(req)
        self._write_response(resp)

    def _read_request(self) -> Request:
        content_len = int(self.headers.get('Content-Length', 0))
        payload = '{}'
        if content_len > 0 and not self.rfile.closed:
            payload = self.rfile.read(content_len).decode('utf-8').strip()
        return Request.from_json_payload(payload)

    def _write_response(self, resp: [Response, None]):
        if resp is None or not isinstance(resp, Response):
            raise TypeError(f'Object is not of type {Response.__base__.__name__}. Got {type(resp)} instead.')

        code_type = type(resp.code)
        if code_type is int:
            status = HTTPStatus(resp.code)
        elif code_type is HTTPStatus:
            status = resp.code
        else:
            msg = f'Response.code is expected to be of type int or http.HTTPStatus but got {code_type} instead.'
            raise TypeError(msg)

        payload = ''
        if resp.body is None or len(resp.body) == 0:
            self.logger.warning('Response.body is either empty or None')
        else:
            payload = json.dumps(resp.body)

        if self.write_delegate is not None:
            self.write_delegate.write(status, payload)
            return
        self.send_response(status)
        self.send_header('Content-Length', str(len(payload)))
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(payload.encode('utf-8'))


def resolve_user_handler(handler_class: Type) -> HandlerBase:
    """
    Constructs a new instance of :class:`HandlerBase` from the provided class.
    :param handler_class: Class from which to construct the :class:`HandlerBase`.
    This must extend :class:`HandlerBase`.
    """

    class H(handler_class):
        def __init__(self):
            self._config = None
            self._logger = None

    if not isinstance(H, ABCMeta):
        msg = f'provided class {H.__base__.__name__} does not extend crowdstrike.foundry.function.HandlerBase'
        raise TypeError(msg)
    h = H()
    if not isinstance(h, HandlerBase):
        msg = f'provided class {H.__base__.__name__} does not extend crowdstrike.foundry.function.HandlerBase'
        raise TypeError(msg)

    h._config = Handler.config
    h._logger = Handler.logger
    h.handler_init()
    return h


def shutdown(*args):
    """Graceful shutdown."""
    print('shutting down now')
    sys.exit(0)
