from io import StringIO
from logging import getLogger
from unittest import main, TestCase
from unittest.mock import patch
from crowdstrike.foundry.function import Function, Response
from crowdstrike.foundry.function.router import Route, Router
from crowdstrike.foundry.function.runner_cli import CLIRunner
from tests.crowdstrike.foundry.function.utils import StaticConfigLoader

if __name__ == '__main__':
    main()


def do_request1(req):
    return Response(
        body={
            'req': req.body,
        },
        code=200,
    )


def do_request2(req, config):
    return Response(
        body={
            'config': config,
            'req': req.body,
        },
        code=200,
    )


def do_request3(req, config, logger):
    return Response(
        body={
            'config': config,
            'logger': logger.name,
            'req': req.body,
        },
        code=200,
    )

def do_request4(req):
    return Response(
        body={
            'req_body': req.body,
            'req_query': req.params.query,
            'req_headers':  req.params.header,
        },
        code=200,
    )


class TestCLIRequestLifecycle(TestCase):
    def setUp(self):
        config = {'a': 'b'}
        router = Router(config)
        router.register(Route(
            method='POST',
            path='/request1',
            func=do_request1,
        ))
        router.register(Route(
            method='POST',
            path='/request2',
            func=do_request2,
        ))
        router.register(Route(
            method='POST',
            path='/request3',
            func=do_request3,
        ))
        router.register(Route(
            method='POST',
            path='/request4',
            func=do_request4,
        ))
        self.runner = CLIRunner()
        self.runner.bind_router(router)
        self.function = Function(
            config_loader=StaticConfigLoader(config),
            router=router,
            runner=self.runner,
        )

    @patch('sys.argv', ['main.py', '--data', './test_data/requests/cli_request1.json'])
    def test_request1(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.function.run()
            resp = mock_stdout.getvalue()
            expected_resp = '\nStatus code: 200\nResponse Header: Content-Length: 50\nResponse Header: Content-Type: application/json\nResponse Payload:\n{"code": 200, "body": {"req": {"hello": "world"}}}\n'
            self.assertEqual(resp, expected_resp, 'Unexpected response received')

    @patch('sys.argv', ['main.py', '--data', './test_data/requests/cli_request2.json'])
    def test_request2(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.function.run()
            resp = mock_stdout.getvalue()
            expected_resp = '\nStatus code: 200\nResponse Header: Content-Length: 72\nResponse Header: Content-Type: application/json\nResponse Payload:\n{"code": 200, "body": {"config": {"a": "b"}, "req": {"hello": "world"}}}\n'
            self.assertEqual(resp, expected_resp, 'Unexpected response received')

    @patch('sys.argv', ['main.py', '--data', './test_data/requests/cli_request3.json'])
    def test_request3(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            use_logger = getLogger('__name__')
            self.function.run(logger=use_logger)
            resp = mock_stdout.getvalue()
            expected_resp = '\nStatus code: 200\nResponse Header: Content-Length: 94\nResponse Header: Content-Type: application/json\nResponse Payload:\n{"code": 200, "body": {"config": {"a": "b"}, "logger": "__name__", "req": {"hello": "world"}}}\n'
            self.assertEqual(resp, expected_resp, 'Unexpected response received')

    @patch('sys.argv', ['main.py', '--data', './test_data/requests/cli_request4.json', '-H', 'X-TEST-HEADER: test', '--header', 'Accept: application/json'])
    def test_request4(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.function.run()
            resp = mock_stdout.getvalue()
            expected_resp = (
                '\nStatus code: 200\nResponse Header: Content-Length: 180\n'
                'Response Header: Content-Type: application/json\n'
                'Response Payload:\n{"code": 200, "body": {"req_body": {"hello": "world"}, '
                '"req_query": {"test": [true], "test2": ["yes"]}, '
                '"req_headers": {"X-Test-Header": ["test"], "Accept": ["application/json"]}}}\n'
            )
            self.assertEqual(expected_resp, resp,'Unexpected response received')

    @patch('sys.argv', ['main.py', '--data', './test_data/requests/cli_request5.json'])
    def test_unknown_endpoint(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.function.run()
            resp = mock_stdout.getvalue()
            expected_resp = '\nStatus code: 404\nResponse Header: Content-Length: 86\nResponse Header: Content-Type: application/json\nResponse Payload:\n{"code": 404, "body": {}, "errors": [{"code": 404, "message": "Not Found: GET /xyz"}]}\n'
            self.assertEqual(resp, expected_resp, 'Unexpected response received')

    @patch('sys.argv', ['main.py', '--data', './test_data/requests/cli_request6.json'])
    def test_unknown_method(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.function.run()
            resp = mock_stdout.getvalue()
            expected_resp = '\nStatus code: 405\nResponse Header: Content-Length: 102\nResponse Header: Content-Type: application/json\nResponse Payload:\n{"code": 405, "body": {}, "errors": [{"code": 405, "message": "Method Not Allowed: GET at endpoint"}]}\n'
            self.assertEqual(resp, expected_resp, 'Unexpected response received')


