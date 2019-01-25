# -*- coding: utf-8 -*-
# File: interface.py

from .config import Config
from .base import ModulesController

__all__ = ['launch_controller_with_config']


def launch_controller_with_config(configuration, ctrl):
    """
    launch with a :class:`Config` and a :class:`ModulesController`.
    It basically does the following
    2 things (and you can easily do them by yourself if you need more control):

    1. extract the input from `configuration.data` .
    2. Call `ctrl.run_pipeline_with_defaults` with rest of the attributes of configuration.

    Args:
        configuration (Config): configuration of modules pipeline
        ctrl (ModulesController): an instance of :class:`ModulesController` (or it's subclasses).

    Example:

    .. code-block:: python

        launch_controller_with_config(
            configuration, )
    """
    assert isinstance(ctrl, ModulesController), ctrl
    assert isinstance(configuration, Config), configuration
    assert configuration.data is not None

    inputs = configuration.data

    ctrl.run_pipeline_with_defaults(
        modules=configuration.modules,
        extra_modules=configuration.extra_modules,
        inputs=inputs
    )

    return ctrl.outputs