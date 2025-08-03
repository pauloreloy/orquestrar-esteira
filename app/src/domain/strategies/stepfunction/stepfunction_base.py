from typing                     import Any, Optional
from src.adapter.aws.aws_client import AWS


class StepFunctionBase:


    def __init__(self, state_machine_name: str):
        self.state_machine_name         = state_machine_name
        self.aws_client: Optional[AWS]  = None

    
    def init_context(self, context):
        if hasattr(context, "aws_client"):
            self.aws_client = context.aws_client


    def execute(self, payload: dict, context: Any = None):
        self.init_context(context)
        self.aws_client.stepfunctions_client.start_execution(self.state_machine_name, payload)
    

    def send_task_failure(self, task_token: str, task_error: str, task_error_cause: str, context: Any = None):
        self.init_context(context)
        self.aws_client.stepfunctions_client.send_task_failure(task_token, task_error, task_error_cause)


    def send_task_success(self, task_token: str, payload: dict, context: Any = None):
        self.init_context(context)
        self.aws_client.stepfunctions_client.send_task_success(task_token, payload)