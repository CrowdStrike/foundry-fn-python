import os
import unittest
from unittest.mock import patch
from crowdstrike.foundry.function.context import ctx_request
from crowdstrike.foundry.function.falconpy import falcon_client
from crowdstrike.foundry.function.model import Request
from falconpy import Hosts

if __name__ == '__main__':
    unittest.main()


class TestFalconClient(unittest.TestCase):

    def setUp(self) -> None:
        ctx_request.set(None)

    def tearDown(self) -> None:
        ctx_request.set(None)

    def test_non_falconpy_class_raises_error(self):
        with self.assertRaisesRegex(TypeError, 'does not extend falconpy.ServiceClass'):
            falcon_client(unittest.TestCase)

    def test_no_request_raises_error(self):
        with self.assertRaisesRegex(AssertionError, 'convenience method requires a request be present'):
            falcon_client(Hosts)

    def test_request_without_access_token_raises_error(self):
        r = Request()
        ctx_request.set(r)
        with self.assertRaisesRegex(AssertionError, 'request must have an access token to use the falcon_client()'):
            falcon_client(Hosts)

    def test_request_with_access_token_returns_prepared_client_at_us1(self):
        ctx_request.set(Request(access_token='foo'))
        client = falcon_client(Hosts)

        self.assertIsInstance(client, Hosts)
        self.assertEqual('Bearer foo', client.headers.get('Authorization'))
        self.assertEqual('https://api.crowdstrike.com', client.base_url)

    def test_request_with_access_token_and_non_default_cloud_returns_prepared_client_at_appropriate_cloud(self):
        ctx_request.set(Request(access_token='foo'))

        tests = [
            {'given': 'us-1', 'expected': 'https://api.crowdstrike.com'},
            {'given': 'us-gov-1', 'expected': 'https://api.laggar.gcw.crowdstrike.com'},
        ]
        for t in tests:
            with patch.dict(os.environ, {'CS_CLOUD': t['given']}, clear=True):
                client = falcon_client(Hosts)

            self.assertIsInstance(client, Hosts)
            self.assertEqual('Bearer foo', client.headers.get('Authorization'))
            self.assertEqual(t['expected'], client.base_url)

    def test_request_inserts_cloud_into_request(self):
        with patch.dict(os.environ, {'CS_CLOUD': 'us-gov-1'}, clear=True):
            ctx_request.set(Request(access_token='foo'))
            client = falcon_client(Hosts)

            self.assertIsInstance(client, Hosts)
            self.assertEqual('Bearer foo', client.headers.get('Authorization'))
            self.assertEqual('https://api.laggar.gcw.crowdstrike.com', client.base_url)
            r = ctx_request.get()
            self.assertEqual('usgov1', r.cloud)
