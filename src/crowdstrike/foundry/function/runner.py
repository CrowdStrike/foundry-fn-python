"""Runner base classes for CrowdStrike Foundry Function FDK."""
import signal
import sys
from abc import ABC, abstractmethod
from crowdstrike.foundry.function.router import Router


class RunnerBase(ABC):
    """Abstract base class for runner implementations."""

    def __init__(self):
        """Initialize the runner."""
        self.router = None

    def bind_router(self, router: Router):
        """Set the router for the runner."""
        self.router = router

    @abstractmethod
    def run(self, *args, **kwargs):
        """Start the runtime."""
        pass


class Runner(RunnerBase):
    """Base class for runner implementations."""

    def __init__(self, runner: RunnerBase = None):
        """Initialize the runner."""
        RunnerBase.__init__(self)
        self._runner = runner

    def run(self, *args, **kwargs):
        """Start the runtime."""
        signal.signal(signal.SIGINT, shutdown)
        signal.signal(signal.SIGTERM, shutdown)

        self._runner.bind_router(self.router)
        return self._runner.run(*args, **kwargs)


def shutdown(*args):
    """Graceful shutdown."""
    print('shutting down now')
    sys.exit(0)
