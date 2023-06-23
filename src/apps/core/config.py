from importlib import import_module

from django.apps import AppConfig


class AppConfigBase(AppConfig):
    """
    app config base class.

    all apps which need to implement a config class, must be subclassed
    from this.
    """

    # the app name.
    name = None

    # fully qualified module names to be imported after app loading.
    # dependencies will be handled by module order as django itself.
    # example: 'src.apps.status.manager'
    required_modules = []

    def _import_modules(self):
        """
        imports all required modules on django startup.
        """

        for module_name in self.required_modules:
            import_module(module_name)

    def _before_import(self):
        """
        performs any operation that should be done before importing modules.

        this method is intended to be overridden by subclasses.
        """
        pass

    def _after_import(self):
        """
        performs any operation that should be done after importing modules.

        this method is intended to be overridden by subclasses.
        """
        pass

    def ready(self):
        """
        This method will let apps do custom operations on django startup.
        If the application is started in migration mode, this operation will
        be skipped.
        """

        # if IS_MIGRATION is not True:
        #     self._before_import()
        #     self._import_modules()
        #     self._after_import()
