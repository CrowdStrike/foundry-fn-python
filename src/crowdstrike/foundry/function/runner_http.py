"""HTTP runner for CrowdStrike Foundry Function FDK."""
import json
import os
from sys import stdout
from http.client import INTERNAL_SERVER_ERROR
from http.server import BaseHTTPRequestHandler, HTTPServer
from logging import Formatter, Logger, StreamHandler, getLogger
import python_multipart
from typing import Dict, List, Union
from crowdstrike.foundry.function.context import ctx_request
from crowdstrike.foundry.function.mapping import canonize_header, dict_to_request, response_to_dict
from crowdstrike.foundry.function.model import APIError, FDKException, Request, Response
from crowdstrike.foundry.function.router import Router
from crowdstrike.foundry.function.runner import RunnerBase


def _new_http_logger() -> Logger:
    f = Formatter('%(asctime)s [%(levelname)s]  %(filename)s %(funcName)s:%(lineno)d  ->  %(message)s')

    h = StreamHandler(stdout)
    h.setFormatter(f)

    logger = getLogger("cs-logger")
    logger.setLevel('DEBUG')
    logger.addHandler(h)
    return logger


class HTTPRunner(RunnerBase):
    """Runs the user's code as part of an HTTP server."""

    def __init__(self):
        """Initialize the HTTP runner."""
        RunnerBase.__init__(self)
        self._port = int(os.environ.get('PORT', '8081'))

    def run(self, *args, **kwargs):
        """Start the HTTP server and listen for requests."""
        logger = kwargs.get('logger', None)
        if logger is None:
            logger = _new_http_logger()
        HTTPRequestHandler.bind_logger(logger)

        HTTPRequestHandler.bind_router(self.router)
        logger.info(f'running at port {self._port}')
        HTTPServer(('', self._port), HTTPRequestHandler).serve_forever()


class HTTPRequestHandler(BaseHTTPRequestHandler):
    """Implements the HTTP request handlers."""

    _logger = None
    _router = None

    @staticmethod
    def bind_logger(logger: Logger):
        """Set the logger to use."""
        HTTPRequestHandler._logger = logger

    @staticmethod
    def bind_router(router: Router):
        """Set the router to use."""
        HTTPRequestHandler._router = router

    def do_DELETE(self):
        """Execute on HTTP DELETE."""
        self._exec_request()

    def do_GET(self):
        """Execute on HTTP GET."""
        self._exec_request()

    def do_HEAD(self):
        """Execute on HTTP HEAD."""
        self._exec_request()

    def do_OPTIONS(self):
        """Execute on HTTP OPTIONS."""
        self._exec_request()

    def do_PATCH(self):
        """Execute on HTTP PATCH."""
        self._exec_request()

    def do_POST(self):
        """Execute on HTTP POST."""
        self._exec_request()

    def do_PUT(self):
        """Execute on HTTP PUT."""
        self._exec_request()

    def _exec_request(self):
        HTTPRequestHandler._logger.info('received request')
        req = self._read_request()
        ctx_request.set(req)
        try:
            resp = HTTPRequestHandler._router.route(req, logger=HTTPRequestHandler._logger)
        except FDKException as fe:
            resp = Response(errors=[APIError(code=fe.code, message=fe.message)])
        self._write_response(req, resp)

    def _read_request(self) -> Request:
        content_type = self.headers.get('Content-Type', 'application/json')
        if not self.rfile.closed:
            if content_type.startswith('multipart/form-data'):
                payload = self._read_multipart_request()
            else:
                payload = self._read_json_request()
            return dict_to_request(payload)
        return dict_to_request('')

    def _read_json_request(self) -> dict:
        content_len = int(self.headers.get('Content-Length', 0))
        payload = self.rfile.read(content_len).decode('utf-8').strip()
        payload = json.loads(payload)
        return payload

    def _read_multipart_request(self) -> dict:
        body = {}
        files = {}
        req = {}

        def on_field(field):
            nonlocal body, req
            fname = field.field_name.decode('utf-8').strip()
            if fname == 'meta':
                value = field.value
                req = json.loads(value.decode('utf-8').strip())
            elif fname == 'body':
                value = field.value
                body = json.loads(value.decode('utf-8').strip())

        def on_file(file):
            nonlocal files  # noqa: F824
            # Offset will currently be at the end of the buffer.
            # Need to reset it to the beginning so we can read it.
            file.file_object.seek(0)
            files[file.file_name.decode('utf-8')] = file.file_object.read(-1)

        python_multipart.parse_form(self.headers, self.rfile, on_field=on_field, on_file=on_file)

        req['body'] = body
        req['files'] = files
        return req

    def _write_response(self, req: Request, resp: Union[Response, None]):
        if resp is None or not isinstance(resp, Response):
            msg = f'Object is not of type {Response.__base__.__name__}. Got {type(resp)} instead.'
            resp = Response(errors=[APIError(code=INTERNAL_SERVER_ERROR, message=msg)])

        if resp.code == 0 and resp.errors is not None and len(resp.errors) > 0:
            for e in resp.errors:
                e_code = e.code
                if type(e_code) is not int and e_code is not None:
                    e_code = int(e_code)
                if type(e_code) is int and 100 <= e.code and resp.code < e.code < 600:
                    resp.code = e_code

        resp.header = self._resp_headers(req, resp)
        payload_dict = response_to_dict(resp)
        payload = json.dumps(payload_dict)

        self.send_response(resp.code)
        self.send_header('Content-Length', str(len(payload)))
        self.send_header('Content-Type', 'application/json')
        for k, v in resp.header.items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(payload.encode('utf-8'))

    def _resp_headers(self, req: Request, resp: Response):
        headers = {}
        if resp.header is not None and len(resp.header) > 0:
            for k, v in resp.header.items():
                if v is None or len(v) == 0:
                    continue
                headers[canonize_header(k)] = v

        if req.params is None or req.params.header is None or len(req.params.header) == 0:
            return headers

        req_header = req.params.header
        self._take_header('X-Cs-Executionid', req_header, headers)
        self._take_header('X-Cs-Origin', req_header, headers)
        self._take_header('X-Cs-Traceid', req_header, headers)

        headers = {k: ';'.join(v) for k, v in headers}
        return headers

    def _take_header(self, key: str, src_header: Dict[str, List[str]], dst_header: Dict[str, List[str]]):
        value = src_header.get(key, [])
        if len(value) == 0:
            return
        dst_header[key] = value
