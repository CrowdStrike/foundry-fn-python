import json
import unittest
from abc import ABC
from http import HTTPStatus
from io import BytesIO
from crowdstrike.foundry.function.handler import Handler
from crowdstrike.foundry.function.handler_base import HandlerBase
from crowdstrike.foundry.function.model import (
    Request,
    Response,
)

if __name__ == '__main__':
    unittest.main()


class TestHandler(unittest.TestCase):

    def setUp(self):
        Handler.handler = None

    def tearDown(self):
        Handler.handler = None

    def test_bind_handler_raises_on_not_abc(self):
        class Foo:
            pass

        self.assertIsNone(Handler.handler)
        with self.assertRaisesRegex(TypeError, 'does not extend crowdstrike.foundry.function.HandlerBase'):
            Handler.bind_handler(Foo)

    def test_bind_handler_raises_on_not_HandlerBase(self):
        class TestABC(ABC):
            pass

        class Foo(TestABC):
            pass

        self.assertIsNone(Handler.handler)
        with self.assertRaisesRegex(TypeError, 'does not extend crowdstrike.foundry.function.HandlerBase'):
            Handler.bind_handler(Foo)

    def test_bind_handler(self):
        class TestFoo(HandlerBase):
            def handle(self, request: Request) -> Response:
                pass

        self.assertIsNone(Handler.handler)
        Handler.bind_handler(TestFoo)
        self.assertIsNotNone(Handler.handler)
        self.assertIsInstance(Handler.handler, TestFoo)

    def test_exec_request(self):
        http_message = (
            'POST / HTTP/1.1\r\n'
            'Host: localhost:8081\r\n'
            'Content-Type: application/json\r\n'
            'Content-Length: 458\r\n'
            '\r\n'
            """{
    "body": {
        "hello": "world"
    },
    "context": {
        "goodnight": "moon"
    },
    "method": "GET",
    "params": {
        "header": {
            "xyz": [
                "a",
                "b"
            ]
        },
        "query": {
            "ijk": [
                "4",
                "5",
                "6"
            ]
        }
    },
    "url": "/qwerty"
}""").encode('utf-8')

        class MockHandler(Handler):
            def setup(self):
                MockHandler.write_delegate = HTTPWriteDelegate()
                self.rfile = BytesIO(http_message)
                self.wfile = BytesIO()

        class MockHandlerBase(HandlerBase):
            def handle(self, request: Request) -> Response:
                return Response(
                    body={'b382b2fb84bb': '38b6af67dc71'},
                    code=HTTPStatus.CREATED,
                )

        MockHandler.load()
        MockHandler.bind_handler(MockHandlerBase)
        MockHandler(None, None, None)._exec_request()

        actual_status = MockHandler.write_delegate.status
        expected_status = HTTPStatus.CREATED
        self.assertEqual(expected_status, actual_status, 'status')

        actual_payload = MockHandler.write_delegate.payload
        expected_payload = json.dumps({'b382b2fb84bb': '38b6af67dc71'})
        self.assertEqual(expected_payload, actual_payload, 'payload')


class HTTPWriteDelegate:

    def __init__(self):
        self.status = None
        self.payload = None

    def write(self, status, payload):
        self.status = status
        self.payload = payload
