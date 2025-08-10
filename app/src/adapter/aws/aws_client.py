from src.adapter.aws.aws_stepfunctions  import StepFunctions
from src.adapter.aws.aws_logs           import Logs


class AWS:


    def __init__(self):
        self.stepfunctions_client   = StepFunctions()
        self.logs_client            = Logs()
