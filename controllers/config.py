# -*- coding: utf-8 -*-
# File: config.py

from utils import mylogger as logger

__all__ = ['Config', 'DEFAULT_MODULES']

# TODO : implement DEFAULT_MODULES()
def DEFAULT_MODULES():
    """
    Return the default Modules,
    which will be used in :class:`Config` and :meth:`ModulesController.run_pipeline_with_defaults`.
    They are:
    1. ParseRequest()
    2. MakeResponse()
    """
    return []


class Config(object):
    """
    A collection of options to be used for ModulesController.
    """

    def __init__(self, data_input=None,modules=None, extra_modules=None,**kwargs):
        """
        Args:
            data_input :
            modules (list): a list of :class:`Module` to perform in pipeline.
            extra_modules (list): the same as ``modules``. This argument
                is only used to provide the defaults in addition to ``modules``.
                The list of modules that will be used in the end is ``modules + extra_modules``.

                It is usually left as None and the default value for this
                option will be the return value of :meth:`ModulesController.DEFAULT_MODULES()`.
                You can override it when you don't like any of the default modules.
        """

        # TODO type checker decorator
        def assert_type(v, tp):
            assert isinstance(v, tp), v.__class__

        self.data = data_input

        if modules is not None:
            assert_type(modules, list)
        self.modules = modules
        if extra_modules is not None:
            assert_type(extra_modules, list)
        self.extra_modules = extra_modules

        if 'name' in kwargs:
            self.pipeline_name = kwargs.pop('name')
        # assert len(kwargs) == 0, "Unknown arguments: {}".format(kwargs.keys())

        logger.logger.info('Initialize Pipeline Configuration')

    def _deprecated_parsing(self):
        self.modules = self.modules or []
        self.extra_modules = DEFAULT_MODULES() if self.extra_modules is None else self.extra_modules
        self.modules.extend(self.extra_modules)

# TODO : implement XmlConfig(Config)
class XmlConfig(Config):
    """
    Same as :class:`Config`, but does the following to automatically
    read and parse config from .xml files:
    """
    pass
