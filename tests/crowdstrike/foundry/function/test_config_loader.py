import os
import unittest
from crowdstrike.foundry.function.config_loader import (
    CONFIG_PATH_ENV_VAR,
    load_config,
)
from unittest.mock import patch

if __name__ == '__main__':
    unittest.main()


def load_test_data_file(file: str) -> str:
    path = os.path.realpath(os.path.dirname(__file__)) + '/../../../..'
    path = os.path.realpath(f'{path}/test_data/config/{file}')
    return path


class TestConfigLoader(unittest.TestCase):

    @patch.dict(os.environ, {CONFIG_PATH_ENV_VAR: ''}, clear=True)
    def test_load_config_returns_none_on_blank_path(self):
        self.assertIsNone(load_config())

    def test_load_config_raises_AssertionError_on_blank_file(self):
        with patch.dict(os.environ, {CONFIG_PATH_ENV_VAR: load_test_data_file('all_blank.json')}, clear=True):
            with self.assertRaises(AssertionError):
                load_config()

    def test_load_config_raises_AssertionError_on_empty_file(self):
        with patch.dict(os.environ, {CONFIG_PATH_ENV_VAR: load_test_data_file('empty.json')}, clear=True):
            with self.assertRaises(AssertionError):
                load_config()

    def test_load_config(self):
        with patch.dict(os.environ, {CONFIG_PATH_ENV_VAR: load_test_data_file('valid.json')}, clear=True):
            actual_config = load_config()
        self.assertIsNotNone(actual_config)
        self.assertTrue(type(actual_config) is dict)

        expected_config = {
            "hostname": "localhost",
            "port": 9876,
        }

        self.assertEqual(expected_config, actual_config,
                         f'expected {expected_config} but got {actual_config}')
