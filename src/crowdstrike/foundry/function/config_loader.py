import logging
from abc import ABC, abstractmethod


class ConfigLoaderBase(ABC):
    """
    Base class for any class which is able to load configuration.
    """

    @abstractmethod
    def load(self, logger: logging.Logger):
        """
        Loads the configuration.
        :param logger: :class:`logging.Logger` instance.
        """
        pass


class ConfigLoader(ConfigLoaderBase):
    """
    Middleware for loading configuration.
    """

    def __init__(self, loader: ConfigLoaderBase):
        """
        :param loader: Desired :class:`ConfigLoaderBase` instance.
        """
        ConfigLoaderBase.__init__(self)
        self._loader = loader

    def load(self, logger: logging.Logger):
        """
        Loads the configuration.
        :param logger: :class:`logging.Logger` instance.
        :returns: Any loaded configuration.
        """
        return self._loader.load(logger)
