
from src.config                                             import params
from typing                                                 import Any, Optional
from src.adapter.aws.aws_client                             import AWS
from src.adapter.quickconfig.quickconfig_adapter            import QuickConfigAdapter
from src.domain.strategies.stepfunction.stepfunction_base   import StepFunctionsBase


class StepFunction(StepFunctionsBase):


    schema                                              = None
    aws_client: Optional[AWS]                           = None
    quickconfig_adapter: Optional[QuickConfigAdapter]   = None
    state_machine_name                                  = None  


    def __init__(self):
        super().__init__()
        
    
    def get_state_machine_name(self, schema):
        toggle_value = self.quickconfig_adapter.get_value(params.TOGGLE_SCHEMAS, params.TOGGLE_DEFAULT)
        return toggle_value.get(self.schema)
    

    def init_context(self, context):
        if hasattr(context, "aws_client"):
            self.aws_client = context.aws_client
        if hasattr(context, "quickconfig_adapter"):
            self.quickconfig_adapter = context.quickconfig_adapter


    def execute(self, payload: dict, context: Any = None):
        self.schema = payload.get("schema")
        _payload    = payload.get("payload")
        self.init_context(context)
        self.state_machine_name = self.get_state_machine_name(self.schema)
        return self.aws_client.stepfunctions_client.start_execution(self.state_machine_name, _payload)