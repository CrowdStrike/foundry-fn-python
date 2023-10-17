from abc import ABC, abstractmethod


class ConfigLoaderBase(ABC):
    """
    Base class for any class which is able to load configuration.
    """

    @abstractmethod
    def load(self):
        """
        Loads the configuration.
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

    def load(self):
        """
        Loads the configuration.
        :returns: Any loaded configuration.
        """
        return self._loader.load()
