import json
import unittest
from crowdstrike.foundry.function.model import (
    APIError,
    Params,
    Request,
)

if __name__ == '__main__':
    unittest.main()


class TestAPIError(unittest.TestCase):
    def test_to_dict(self):
        actual = APIError(
            code=123,
            message='hello world',
        ).to_dict()
        expected = {
            'code': 123,
            'message': 'hello world',
        }

        self.assertEqual(expected, actual, f'expected={expected} but got {actual}')


class TestRequest(unittest.TestCase):

    def test_from_json_payload(self):
        expected = Request(
            body={
                'hello': 'world',
            },
            context={
                'goodnight': 'moon',
            },
            method='GET',
            params=Params(
                header={
                    'Accepts': ['application/json'],
                    'Content-Type': ['application/json'],
                    'Xyz': ['a', 'b'],
                },
                query={
                    'ijk': ['4', '5', '6'],
                },
            ),
            url='/qwerty',
        )

        payload = json.dumps({
            'body': {
                'hello': 'world',
            },
            'context': {
                'goodnight': 'moon',
            },
            'method': 'GET',
            'params': {
                'header': {
                    'accepts': ['application/json'],
                    'ContENt-type': ['application/json'],
                    'xyz': ['a', 'b'],
                },
                'query': {
                    'ijk': ['4', '5', '6'],
                },
            },
            'url': '/qwerty',
        })
        actual = Request.from_json_payload(payload)

        self.assertEqual(expected, actual, f'expected={expected} but got {actual}')
