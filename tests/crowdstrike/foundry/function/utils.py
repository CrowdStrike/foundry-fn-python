import logging

from crowdstrike.foundry.function.config_loader import ConfigLoaderBase
from crowdstrike.foundry.function.runner import RunnerBase


class CapturingRunner(RunnerBase):

    def __init__(self):
        RunnerBase.__init__(self)
        self.response = None

    def run(self, *args, **kwargs):
        self.response = self.router.route(args[0])


class StaticConfigLoader(ConfigLoaderBase):

    def __init__(self, config):
        self.config = config

    def load(self, logger: logging.Logger):
        return self.config
