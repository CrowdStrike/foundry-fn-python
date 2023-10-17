import json
import os
from crowdstrike.foundry.function.config_loader import ConfigLoaderBase


class FileSystemConfigLoader(ConfigLoaderBase):
    """
    Loads configuration from the local filesystem.
    """

    def __init__(self):
        ConfigLoaderBase.__init__(self)

    def load(self):
        """
        Loads the configuration located at the path specified in the `CS_FN_CONFIG_PATH` environment variable.
        The path may be either relative or absolute.
        If the environment variable is not provided, no configuration will be loaded.
        :returns: Any loaded configuration.
        """
        file_path = os.environ.get('CS_FN_CONFIG_PATH', None)
        if file_path is None:
            return None

        if not os.path.exists(file_path):
            raise FileNotFoundError(file_path)

        with open(file_path) as fp:
            contents = ' '.join(fp.readlines())

        return json.loads(contents)
