from crowdstrike.foundry.function.falconpy import falcon_client
from crowdstrike.foundry.function.model import *


class Function:
    """
    Represents a Function.
    """

    _instance: ['Function', None] = None

    @staticmethod
    def instance(
            module: str = '',
            config=None,
            config_loader=None,
            loader=None,
            logger=None,
            router=None,
            runner=None,
    ) -> 'Function':
        """
        Fetch the singleton instance of the :class:`Function`, creating one if one does not yet exist.
        :param module: Name of the module in which code should be imported.
        :param config: Configuration to provide to the user's code.
        :param config_loader: :class:`ConfigLoaderBase` instance capable of loading configuration if `config` is None.
        :param loader: :class:`Loader` instance.
        :param logger: :class:`logging.Logger` instance.
        :param router: :class:`Router` instance.
        :param runner: :class:`RunnerBase` instance.
        :returns: :class:`Function` singleton.
        """
        if Function._instance is None:
            Function._instance = Function(
                module=module,
                config=config,
                config_loader=config_loader,
                loader=loader,
                logger=logger,
                router=router,
                runner=runner,
            )
        return Function._instance

    def __init__(
            self,
            module: str = '',
            config=None,
            config_loader=None,
            loader=None,
            logger=None,
            router=None,
            runner=None,
    ):
        """
        :param module: Name of the module in which code should be imported.
        :param config: Configuration to provide to the user's code.
        :param config_loader: :class:`ConfigLoaderBase` instance capable of loading configuration if `config` is None.
        :param loader: :class:`Loader` instance.
        :param logger: :class:`logging.Logger` instance.
        :param router: :class:`Router` instance.
        :param runner: :class:`RunnerBase` instance.
        """
        self._config = config
        self._loader = loader
        self._logger = logger
        self._router = router
        self._runner = runner

        if self._logger is None:
            from crowdstrike.foundry.function.cslogger import new_logger
            self._logger = new_logger()
        if self._config is None:
            if config_loader is None:
                from crowdstrike.foundry.function.config_loader import ConfigLoader
                from crowdstrike.foundry.function.config_loader_fs import FileSystemConfigLoader
                config_loader = ConfigLoader(FileSystemConfigLoader())
            self._config = config_loader.load(self._logger)
        if self._loader is None:
            from crowdstrike.foundry.function.loader import Loader
            self._loader = Loader()
        if self._router is None:
            from crowdstrike.foundry.function.router import Router
            self.router = Router(self._logger, self._config)
        if self._runner is None:
            from crowdstrike.foundry.function.runner import Runner
            from crowdstrike.foundry.function.runner_http import HTTPRunner
            self._runner = Runner(HTTPRunner())
            self._runner.bind_logger(self._logger)
            self._runner.bind_router(self._router)

        self._loader.register_module(module)

    def run(self, *args, **kwargs):
        """
        Runs the function. Essentially the "main" method of the function.
        Any arguments provided to this method are forwarded directly down into :class:`RunnerBase` instance.
        :return: Any result from the given :class:`RunnerBase` instance.
        """
        self._loader.load()
        return self._runner.run(*args, **kwargs)

    def handler(self, method: str, path: str, provide_logger: bool = True, provide_config: bool = True):
        """
        Decorator for handlers.
        :param method: HTTP method or verb to bind to this handler.
        :param path: URL path at which this handler resides.
        :param provide_config: Whether this handler should receive any loaded configuration.
        :param provide_logger: Whether this handler should receive a :class:`logging.Logger` instance.
        """

        def call(func):
            from crowdstrike.foundry.function.router import Route
            self._router.register(Route(
                func=func,
                method=method,
                path=path,
                provide_logger=provide_logger,
                provide_config=provide_config,
            ))

        return call
