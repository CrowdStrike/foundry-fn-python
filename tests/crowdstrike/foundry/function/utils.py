from crowdstrike.foundry.function.config_loader import ConfigLoaderBase
from crowdstrike.foundry.function.runner import RunnerBase


class CapturingRunner(RunnerBase):

    def __init__(self):
        RunnerBase.__init__(self)
        self.logger = None
        self.response = None

    def run(self, *args, **kwargs):
        self.logger = kwargs.get('logger', None)
        self.response = self.router.route(args[0], logger=self.logger)


class StaticConfigLoader(ConfigLoaderBase):

    def __init__(self, config):
        self.config = config

    def load(self):
        return self.config
