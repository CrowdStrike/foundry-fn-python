import signal
import sys
from abc import ABC, abstractmethod
from crowdstrike.foundry.function.router import Router


class RunnerBase(ABC):
    def __init__(self):
        self.router = None

    def bind_router(self, router: Router):
        self.router = router

    @abstractmethod
    def run(self, *args, **kwargs):
        pass


class Runner(RunnerBase):

    def __init__(self, runner: RunnerBase = None):
        RunnerBase.__init__(self)
        self._runner = runner

    def run(self, *args, **kwargs):
        """
        Starts runtime.
        """

        signal.signal(signal.SIGINT, shutdown)
        signal.signal(signal.SIGTERM, shutdown)

        self._runner.bind_router(self.router)
        return self._runner.run(*args, **kwargs)


def shutdown(*args):
    """Graceful shutdown."""
    print('shutting down now')
    sys.exit(0)
