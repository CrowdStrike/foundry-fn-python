import json
import os
from logging import Logger
from typing import (
    Any,
    Dict,
)

CONFIG_PATH_ENV_VAR = 'CS_FN_CONFIG_PATH'


def load_config(logger: [Logger, None] = None) -> [Dict[str, Any], None]:
    """
    Loads configuration.
    :param logger: `Logger` instance.
    :return: Any loaded configuration as a dict, or None if no value exists for the CS_FN_CONFIG_PATH environment
    variable.
    :raises AssertionError: Successfully read the configuration file but the file was considered empty.
    """
    config_path = os.environ.get(CONFIG_PATH_ENV_VAR, '')
    if config_path is None or config_path.strip() == '':
        msg = f'No value provided for configuration environment variable "{CONFIG_PATH_ENV_VAR}".' \
              ' Configuration will be None.'
        if logger is None:
            print(msg)
        else:
            logger.warning(msg)
        return None

    with open(config_path.strip()) as fp:
        contents = ''.join(line.strip() for line in fp.readlines())

    if contents == '':
        msg = f'successfully read configuration file "{config_path.strip()}" but no non-blank lines were read'
        raise AssertionError(msg)
    return json.loads(contents)
