from crowdstrike.foundry.function import Function, Request, Response, FDKException
from crowdstrike.foundry.function.cslogger import new_logger
from crowdstrike.foundry.function.router import Route, Router
from tests.crowdstrike.foundry.function.utils import CapturingRunner, StaticConfigLoader
from unittest import main, TestCase

if __name__ == '__main__':
    main()

logger = new_logger()


def do_request_config_logger(req, config, l):
    return Response(
        body={
            'config': config,
            'req': req.body,
            'has_logger': l is not None,
        },
        code=200,
    )


def do_request_config(req, config):
    return Response(
        body={
            'config': config,
            'req': req.body,
            'has_logger': False,
        },
        code=200,
    )


def do_request_logger(req, l):
    return Response(
        body={
            'config': None,
            'req': req.body,
            'has_logger': l is not None,
        },
        code=200,
    )


def do_request(req):
    return Response(
        body={
            'config': None,
            'req': req.body,
            'has_logger': False,
        },
        code=200,
    )


class TestRequestResponse(TestCase):

    def setUp(self):
        config = {'a': 'b'}
        router = Router(logger, config)
        router.register(Route(
            method='GET',
            path='/only_request',
            func=do_request,
            provide_config=False,
            provide_logger=False,
        ))
        router.register(Route(
            method='POST',
            path='/request_and_logger',
            func=do_request_logger,
            provide_config=False,
            provide_logger=True,
        ))
        router.register(Route(
            method='PUT',
            path='/request_and_config',
            func=do_request_config,
            provide_config=True,
            provide_logger=False,
        ))
        router.register(Route(
            method='DELETE',
            path='/request_and_config_and_logger',
            func=do_request_config_logger,
            provide_config=True,
            provide_logger=True,
        ))
        self.runner = CapturingRunner()
        self.runner.bind_router(router)
        self.runner.bind_logger(logger)
        self.function = Function(
            config_loader=StaticConfigLoader(config),
            router=router,
            runner=self.runner,
        )

    def test_only_request(self):
        req = Request(
            body={'hello': 'world'},
            method='GET',
            url='/only_request',
        )
        self.function.run(req)
        resp = self.runner.response
        self.assertIsNotNone(resp, 'response is none')
        self.assertEqual(200, resp.code, f'expected response of 200 but got {resp.code}')
        self.assertDictEqual(
            {'config': None, 'req': {'hello': 'world'}, 'has_logger': False},
            resp.body,
            'actual body differs from expected body'
        )

    def test_request_logger(self):
        req = Request(
            body={'hello': 'world'},
            method='POST',
            url='/request_and_logger',
        )
        self.function.run(req)
        resp = self.runner.response
        self.assertIsNotNone(resp, 'response is none')
        self.assertEqual(200, resp.code, f'expected response of 200 but got {resp.code}')
        self.assertDictEqual(
            {'config': None, 'req': {'hello': 'world'}, 'has_logger': True},
            resp.body,
            'actual body differs from expected body'
        )

    def test_request_config(self):
        req = Request(
            body={'hello': 'world'},
            method='PUT',
            url='/request_and_config',
        )
        self.function.run(req)
        resp = self.runner.response
        self.assertIsNotNone(resp, 'response is none')
        self.assertEqual(200, resp.code, f'expected response of 200 but got {resp.code}')
        self.assertDictEqual(
            {'config': {'a': 'b'}, 'req': {'hello': 'world'}, 'has_logger': False},
            resp.body,
            'actual body differs from expected body'
        )

    def test_request_config_logger(self):
        req = Request(
            body={'hello': 'world'},
            method='DELETE',
            url='/request_and_config_and_logger',
        )
        self.function.run(req)
        resp = self.runner.response
        self.assertIsNotNone(resp, 'response is none')
        self.assertEqual(200, resp.code, f'expected response of 200 but got {resp.code}')
        self.assertDictEqual(
            {'config': {'a': 'b'}, 'req': {'hello': 'world'}, 'has_logger': True},
            resp.body,
            'actual body differs from expected body'
        )

    def test_unknown_endpoint(self):
        with self.assertRaisesRegex(FDKException, "Not Found: /xyz"):
            req = Request(
                body={'hello': 'world'},
                method='GET',
                url='/xyz',
            )
            self.function.run(req)

    def test_unknown_method(self):
        with self.assertRaisesRegex(FDKException, "Method Not Allowed: GET"):
            req = Request(
                body={'hello': 'world'},
                method='GET',
                url='/request_and_config_and_logger',
            )
            self.function.run(req)
