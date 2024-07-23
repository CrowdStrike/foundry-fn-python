import os
from crowdstrike.foundry.function import Function, Request, Response, FDKException, cloud
from crowdstrike.foundry.function.router import Route, Router
from logging import Logger
from tests.crowdstrike.foundry.function.utils import CapturingRunner, StaticConfigLoader
from unittest import main, TestCase
from unittest.mock import patch

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
            'logger': logger,
            'req': req.body,
        },
        code=200,
    )


class TestRequestLifecycle(TestCase):
    logger = Logger(__name__)

    def setUp(self):
        config = {'a': 'b'}
        router = Router(config, self.logger)
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
        self.runner = CapturingRunner()
        self.runner.bind_router(router)
        self.function = Function(
            config_loader=StaticConfigLoader(config),
            router=router,
            runner=self.runner,
        )

    def test_request1(self):
        req = Request(
            body={'hello': 'world'},
            method='POST',
            url='/request1',
        )
        self.function.run(req)
        resp = self.runner.response
        self.assertIsNotNone(resp, 'response is none')
        self.assertEqual(200, resp.code, f'expected response of 200 but got {resp.code}')
        self.assertDictEqual(
            {'req': {'hello': 'world'}},
            resp.body,
            'actual body differs from expected body'
        )

    def test_request2(self):
        req = Request(
            body={'hello': 'world'},
            method='POST',
            url='/request2',
        )
        self.function.run(req)
        resp = self.runner.response
        self.assertIsNotNone(resp, 'response is none')
        self.assertEqual(200, resp.code, f'expected response of 200 but got {resp.code}')
        self.assertDictEqual(
            {'config': {'a': 'b'}, 'req': {'hello': 'world'}},
            resp.body,
            'actual body differs from expected body'
        )

    def test_request3(self):
        req = Request(
            body={'hello': 'world'},
            method='POST',
            url='/request3',
        )
        self.function.run(req)
        resp = self.runner.response
        self.assertIsNotNone(resp, 'response is none')
        self.assertEqual(200, resp.code, f'expected response of 200 but got {resp.code}')
        self.assertDictEqual(
            {
                'config': {'a': 'b'},
                'logger': self.logger,
                'req': {'hello': 'world'},
            },
            resp.body,
            'actual body differs from expected body'
        )

    def test_unknown_endpoint(self):
        with self.assertRaisesRegex(FDKException, "Not Found: GET /xyz"):
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
                url='/request1',
            )
            self.function.run(req)


class TestCloud(TestCase):

    def test_cloud_returns_default_if_none_specified(self):
        with patch.dict(os.environ, {}, clear=True):
            c = cloud()
            self.assertEqual("auto", c)

    def test_cloud_returns_cloud_in_env(self):
        with patch.dict(os.environ, {'CS_CLOUD': 'us-gov-1'}, clear=True):
            c = cloud()
            self.assertEqual("usgov1", c)
