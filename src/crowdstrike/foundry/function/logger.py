import logging
import os
import sys
from typing import (
    Any,
)


def get_log_level() -> str:
    """
    Determines the log level.  Will default to INFO.
    :return: Log level.
    """
    return _get_log_level(os.environ.get('LOG_LEVEL'))


def _get_log_level(env_log_lvl):
    log_lvl = 'INFO'

    if type(env_log_lvl) is str and env_log_lvl.upper() in {'DEBUG', 'INFO', 'WARN', 'WARNING', 'ERROR', 'CRITICAL'}:
        env_log_lvl = env_log_lvl.upper()
        log_lvl = 'WARNING' if env_log_lvl == 'WARN' else env_log_lvl
    else:
        print('unknown log level from env variable LOG_LEVEL:', str(env_log_lvl), 'defaulting to', log_lvl)
    print('using log level', str(log_lvl))

    return log_lvl


def new_logger() -> logging.Logger:
    """
    Constructs a new, initialized logger instance.
    :return: `logging.Logger`.
    """
    handler = logging.StreamHandler(sys.stdout)
    fmt = logging.Formatter('[%(asctime)s %(levelname)s] - %(message)s')
    handler.setFormatter(fmt)
    log = CSLogger(__name__, get_log_level())
    log.addHandler(handler)
    return log


class CSLogger(logging.Logger):
    """
    Logger instance with some enhancements.
    """

    def __init__(self, name, level):
        """
        :param name: Logger name.
        :param level: Log level.
        """
        logging.Logger.__init__(self, name, level.upper())
        self._level = level.upper()
        self._extras = {}
        self._logger = logging.Logger(name, self._level)
        self._name = name

    def addHandler(self, hdlr: logging.Handler):
        logging.Logger.addHandler(self, hdlr)
        self._logger.addHandler(hdlr)

    def extra(self, key: str, value: [str, None]) -> 'CSLogger':
        """
        Adds any extra (key, value) pair that the author would like to include when logging.
        Provide a value of `None` to remove the key from the collection.
        :param key: Key to log.
        :param value: Value to log.
        :return: Clone of self with the modification.
        """
        extras = self._extras
        if value is None:
            if key in self._extras:
                del extras[key]
        else:
            self._extras[key] = value
        clone = self._clone(False)
        clone._extras = extras
        return clone

    def critical(self, msg, *args, **kwargs):
        self._logger.critical(self._prepare_msg(msg), *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        self._logger.debug(self._prepare_msg(msg), *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self._logger.error(self._prepare_msg(msg), *args, **kwargs)

    def exception(self, msg, *args, **kwargs):
        self._logger.exception(self._prepare_msg(msg), *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self._logger.info(self._prepare_msg(msg), *args, **kwargs)

    def warn(self, msg, *args, **kwargs):
        self.warning(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self._logger.warning(self._prepare_msg(msg), *args, **kwargs)

    def _prepare_msg(self, msg: [str, Any]) -> str:
        msg_dict = {**self._extras, **{'msg': msg}}
        msg_str = '\t'.join(f'{k}={v}' for k, v in msg_dict.items())
        return msg_str

    def _clone(self, include_extras: bool) -> 'CSLogger':
        clone = CSLogger(self._name, self._level)
        for h in self.handlers:
            clone.addHandler(h)
        if include_extras:
            clone._extras = {**self._extras, **{}}
        return clone
