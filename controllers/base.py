# -*- coding: utf-8 -*-
# File: base.py

import weakref
import six
from abc import abstractmethod, ABCMeta
import copy

from modules import (Module, Modules)
from utils import mylogger as logger
from utils.argtools import call_only_once

from .config import Config, DEFAULT_MODULES

__all__ = ['Stop', 'ModulesController']


class Stop(Exception):
    """
    An exception thrown to stop pipeline.
    """
    pass


class ModulesController(object):
    """ Base class for a ModulesController.
    """

    # is_chief = True
    # """
    # Whether this process is the chief worker in multi-pipeline.
    # Certain Modules will only be run by chief worker.
    # """

    def __init__(self):
        self._modules = []
        self.ModuleTable = {}

    @call_only_once
    def build_pipeline(self, modules):
        """
        Setup Modules to built the modules pipeline.

        Args:
            modules ([Module]): list of Module instances
        """
        assert isinstance(modules, list), modules

        for md in modules:
            self.Check_Module(md)

        # some final operations that might modify the pipeline
        logger.logger.info("Build Modules pipeline ...")
        self._modules = Modules(self._modules)
        self._modules.register_to_controller(weakref.proxy(self))
        self._modules = self._modules.get_modules()

    def run_pipeline(self,modules,inputs):
        """
        Implemented by two lines:

        .. code-block:: python

            self.build_pipeline(modules)
            self.main_loop(inputs)

        You can call those methods by yourself to have better control on details if needed.
        """

        self.build_pipeline(modules)
        self.main_loop(inputs)

    def run_pipeline_with_defaults(self, modules=None, extra_modules=None,inputs=None):
        """
        Same as :meth:`run_pipeline()`, except:

        1. Add `extra_modules` to modules. The default value for
           `extra_modules` is :meth:`DEFAULT_MODULES()`.
        """

        modules = copy.copy(modules or [])
        extra_modules = DEFAULT_MODULES() if extra_modules is None else extra_modules
        modules.extend(extra_modules)

        self.run_pipeline(modules,inputs)

    @call_only_once
    def main_loop(self, inputs):
        """
        Run the main piepline loop.

        Args:
            inputs (tuple): inputs must be a tuple(thus we can treat multi-input and multi-output)
        """
        logger.logger.info("Begin Modules pipeline ...")
        for index, cb in enumerate(self._modules):
            inputs = self.run_step(inputs, index)

        self.outputs = inputs

    def run_step(self,inputs,index):
        """
        Defines what to do in one stage of pipeline. The default is:
        '' run one module ''.

        The behavior of each iteration can be changed by overriding this method.
        """
        #TODO 如何使得当前模块的输入只用到前一个模块的部分输出？
        if index != 0:
            current_module_input_desc = self.ModuleTable[
                self._modules[index].__class__.__name__].get_inputs_desc()

            pre_module_output_desc = self.ModuleTable[
                self._modules[index-1].__class__.__name__].get_outputs_desc()

            if not current_module_input_desc==pre_module_output_desc:
                raise Stop(
                    'module {} and {} can\'t be pipelined ,it may be caused by inconsistent input and output.'
                    'check description of those modules for details.'
                    .format(self._modules[index-1].__class__.__name__,self._modules[index].__class__.__name__))

        if not type(inputs)==type(tuple):
            inputs = (inputs,)
        return self._modules[index].run(inputs)

    def _Check_Module(self, md):
        """
        Check Modules which are passed to ModulesController by Config.
        It can only be called before :meth:`ModulesController.run_pipeline()`.

        Args:
            md (Module or [Module]): a Module or a list of Modules

        Returns:
            succeed or not
        """
        if isinstance(md, (list, tuple)):
            for x in md:
                self._Check_Module(x)
            return
        assert isinstance(md, Module), md
        assert not isinstance(self._modules, Modules), \
            "Cannot append more Modules after ModulesController was setup!"
        self._modules.append(md)
        return True

    Check_Module = _Check_Module

    def register_ModuleDesc_to_ModuleTable(self,Module_name,desc):
        self.ModuleTable[Module_name] = desc

    def __new__(cls, *args, **kwargs):
        if (len(args) > 0 and isinstance(args[0], Config)) \
                or 'config' in kwargs:
            logger.logger.error("Use interface API to launch controller ,do not pass Config directly to a controller!")
            import sys
            sys.exit(1)
        else:
            return super(ModulesController, cls).__new__(cls)


# TODO : implement class WebAPI()
# TODO : input(eg: request) should be processed before passing it to the pipeline ?
@six.add_metaclass(ABCMeta)
class WebAPI(ModulesController):
    """
        Base class for WebAPI 's ModulesController.

        ModulesController  for WebAPI has a :meth:`setup_input` method which parse request

        """
    # TODO : implement function setup_input()
    def setup_input(self,request):
        raise NotImplementedError



