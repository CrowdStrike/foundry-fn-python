class Loader:
    """
    Module loader.
    """

    def __init__(self):
        self._modules = set()

    def register_module(self, module: str):
        """
        Registers a module to be loaded at function run.
        :param module: Name of the module. If the empty string or `__main__`, will ignore.
        """
        if module == '' or module == '__main__':
            return
        self._modules.add(module)

    def load(self):
        """
        Loads any registered modules.
        """
        from importlib import import_module
        for m in self._modules:
            import_module(m)
