import json
import os
from crowdstrike.foundry.function.context import ctx_request
from crowdstrike.foundry.function.mapping import canonize_header, dict_to_request, response_to_dict
from crowdstrike.foundry.function.model import APIError, FDKException, Request, Response
from crowdstrike.foundry.function.router import Router
from crowdstrike.foundry.function.runner import RunnerBase
from http.client import INTERNAL_SERVER_ERROR
from http.server import BaseHTTPRequestHandler, HTTPServer


class HTTPRunner(RunnerBase):
    """
    Runs the user's code as part of an HTTP server.
    """

    def __init__(self):
        RunnerBase.__init__(self)
        self._port = int(os.environ.get('PORT', '8081'))

    def run(self):
        print(f'running at port {self._port}')
        HTTPRequestHandler.bind_router(self.router)
        HTTPServer(('', self._port), HTTPRequestHandler).serve_forever()


class HTTPRequestHandler(BaseHTTPRequestHandler):
    _router = None

    @staticmethod
    def bind_router(router: Router):
        HTTPRequestHandler._router = router

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
        print('received request')
        req = self._read_request()
        ctx_request.set(req)
        try:
            resp = HTTPRequestHandler._router.route(req)
        except FDKException as fe:
            resp = Response(errors=[APIError(code=fe.code, message=fe.message)])
        self._write_response(req, resp)

    def _read_request(self) -> Request:
        content_len = int(self.headers.get('Content-Length', 0))
        payload = '{}'
        if content_len > 0 and not self.rfile.closed:
            payload = self.rfile.read(content_len).decode('utf-8').strip()
        payload = json.loads(payload)
        return dict_to_request(payload)

    def _write_response(self, req: Request, resp: [Response, None]):
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

    def _take_header(self, key: str, src_header: dict[str, list[str]], dst_header: dict[str, list[str]]):
        value = src_header.get(key, [])
        if len(value) == 0:
            return
        dst_header[key] = value
