from abc import ABC
from argparse import ArgumentParser
from http.server import HTTPServer
from crowdstrike.foundry.function.handler import Handler
from crowdstrike.foundry.function.handler_base import HandlerBase as PySlHandlerBase
from crowdstrike.foundry.function.logger import new_logger
from crowdstrike.foundry.function.model import (
    Request,
    Response,
)
from typing import Type


def run():
    """
    Driver function.
    """
    parser = ArgumentParser()
    parser.add_argument('-p', '--port',
                        default=8081,
                        type=int,
                        help='port on which to start the test HTTP server (default 8081)')
    args = parser.parse_args()

    if not 1024 <= args.port < 65536:
        raise AssertionError('port must be in range [1024, 65536)')

    Handler.logger.info(f'starting server at localhost:{args.port}')
    HTTPServer(('0.0.0.0', args.port), Handler).serve_forever()


class HandlerBase(PySlHandlerBase, ABC):
    """
    Base class for custom SDK handlers.
    """
    pass


class CSHandler:
    """
    CrowdStrike SDK handler driver.
    """
    bootstrapped: bool = False

    @staticmethod
    def bootstrap(handler_class: Type):
        """
        Bootstraps the CSHandler class by loading any needed configuration, creating loggers,
        and constructing an instance of the handler.
        :param handler_class: Class from which to construct the :class:`HandlerBase`.
        This must extend :class:`HandlerBase`.
        """
        if not CSHandler.bootstrapped:
            Handler.load()
            Handler.bind_handler(handler_class)
            Handler.bootstrapped = True
