import unittest
from crowdstrike.foundry.function.cslogger import (
    CSLogger,
    _get_log_level,
)

if __name__ == '__main__':
    unittest.main()


class TestLoggerUtilities(unittest.TestCase):

    def test__get_log_level(self):
        given_expects = {
            'CRITICAL': 'CRITICAL',
            'DEBUG': 'DEBUG',
            'ERROR': 'ERROR',
            'INFO': 'INFO',
            'WARN': 'WARNING',
            'WARNING': 'WARNING',
            'QWERTY': 'INFO',
        }
        for given, expects in given_expects.items():
            given_upper = given.upper()
            given_lower = given.lower()

            actual = _get_log_level(given_upper)
            self.assertEqual(expects, actual, f'given "{given_upper}"')
            actual = _get_log_level(given_lower)
            self.assertEqual(expects, actual, f'given "{given_lower}"')


class TestLogger(unittest.TestCase):

    def test__prepare_msg(self):
        log = CSLogger(__name__, 'INFO')
        self.assertEqual('msg=hello', log._prepare_msg('hello'))
