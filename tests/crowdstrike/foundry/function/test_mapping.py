import unittest
from crowdstrike.foundry.function.model import (
    RequestParams,
    Request,
)
from crowdstrike.foundry.function.mapping import (
    dict_to_request,
)

if __name__ == '__main__':
    unittest.main()


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
            params=RequestParams(
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

        payload = {
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
        }
        actual = dict_to_request(payload)

        self.assertEqual(expected, actual, f'expected={expected} but got {actual}')
