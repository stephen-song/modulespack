from modules import Module,ModuleDesc,InputDesc,OutputDesc
import numpy as np

class add(Module):

    def __init__(self):
        pass

    def _make_module_description(self):
        inputdesc = InputDesc(
            datatype=np.float32,datashape=(None,),name='x')

        outputdesc = OutputDesc(
            datatype=np.float32,datashape=(None,),name='y')

        config = ModuleDesc(inputdesc,outputdesc)
        return config

    @staticmethod
    def _run(inputs):
        ret = inputs[0]
        ret = ret + 2.
        # print('add_')
        return ret