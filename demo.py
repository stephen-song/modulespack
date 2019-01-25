from controllers import ModulesController,launch_controller_with_config,Config
from modules.ModuleLib import add,divide,add2

modules = [add2(),divide()]

PipelineConfig = Config(data_input=15.0,modules=modules)

controller = ModulesController()

result = launch_controller_with_config(PipelineConfig,controller)

print(result)
