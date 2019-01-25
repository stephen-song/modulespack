# -*- coding: utf-8 -*-
# File: base.py

from abc import ABCMeta
import six
from utils import mylogger as logger

__all__ = ['Module', 'ProxyModule', 'ModuleFactory']

# TODO : write help_doc in  http://xx.html
@six.add_metaclass(ABCMeta)
class Module(object):
    """ Base class for all Modules. See
    `Write a Module
    <http://xx.html>`_
    for more detailed explanation of the module methods.

    Attributes:
        controller(ModuleController): the controller of all modules used in a specific Web API.
        module_description(ModuleDesc): the description of current module.

    Note:
        These attributes are available only after (and including)
        :meth:`_register_to_controller`.

    .. document private functions
    .. automethod:: _get_module_description
    .. automethod:: _make_module_description
    .. automethod:: _register_to_controller
    .. automethod:: _run

    """

    # _chief_only = True

    def _get_module_description(self):
        logger.logger.info('Instantiate ModuleDesc for '+str(self.__class__.__name__))
        if hasattr(self,'module_description'):
            pass
        else :
            self.module_description = self._make_module_description()
        return self.module_description

    def _make_module_description(self):
        """
        Override this method to setup the descriptions of the Module.

        Note : The return value must be a instance of ModuleDesc.

        Examples:
            def _make_module_description(self):
                inputdesc = InputDesc(datatype=np.float32,datashape=(None,),name='x')
                outputdesc = OutputDesc(datatype=np.float32,datashape=(None,),name='y')
                desc = ModuleDesc(inputdesc,outputdesc)
                return desc
        """
        raise NotImplementedError('you must override function _make_module_description() in your subclass and return instance of ModuleDesc')


    def register_to_controller(self, controller):
        self.controller = controller
        self._register_to_controller()
        logger.logger.info('Register ' + str(self.__class__.__name__) + ' to controller')

    def _register_to_controller(self):
        """
        Called before finalizing the registration.
        This method will register the description to a ModuleTable(dict-like) which is managed by Module's controller.
        Thus, controller can find the corresponding desc by class name in ModuleTable.
        """
        self.controller.register_ModuleDesc_to_ModuleTable(self.__class__.__name__,self._get_module_description())


    def run(self,inputs):
        logger.logger.info('Run '+str(self.__class__.__name__))
        ret = self._run(inputs)
        return ret

    def _run(self,inputs):
        """
        Override this method to implement the functionality that this module should have.

        Note :
            Inputs is something like a tuple, the order of elements in inputs must be the same as they are defined in inputdesc.
            The return value must be something like a tuple. Elements order of outputs should also meet the definition!

        Examples:
            class new_module(Module):

                def _make_module_description(self):
                    inputdesc = [InputDesc(datatype=np.float32,datashape=(None,),name='x1'),
                                InputDesc(datatype=np.float32,datashape=(None,),name='x2')]
                    outputdesc = [OutputDesc(datatype=np.float32,datashape=(None,),name='y1'),
                                OutputDesc(datatype=np.float32,datashape=(None,),name='y2')]
                    desc = ModuleDesc(inputdesc,outputdesc)
                    return desc

                def _run(inputs):
                    x1 = inputs[0]
                    x2 = inputs[1]
                    y1 = x2
                    y2 = x1
                    return y1,y2   # Error example: return y2,y1 #
        """
        raise NotImplementedError('you must override function _run() in your subclass')


    def __str__(self):
        return type(self).__name__


class ProxyModule(Module):
    """ A Module which proxy all methods to another Module.
        It's useful as a base class of Modules which decorate other Modules.
    """
    def __init__(self, cb,*args,**kwargs):
        """
        Args:
            cb(Module): the underlying Module
        """
        assert isinstance(cb, Module), type(cb)
        self.cb = cb
        #TODO 对多余参数的处理

    def __str__(self):
        return "Proxy-" + str(self.cb)


class ModuleFactory(Module):
    """
    Create a Module with some lambdas.
    """
    def __init__(self, make_module_description=None, run=None):
        """
        Each lambda takes ``self`` as the only argument.
        """

        self._cb_make_module_description = make_module_description
        self._cb_run = run

    def _make_module_description(self):
        if self._cb_make_module_description:
            return self._cb_make_module_description(self)

    def _run(self,inputs):
        if self._cb_run:
            return self._cb_run(inputs)

