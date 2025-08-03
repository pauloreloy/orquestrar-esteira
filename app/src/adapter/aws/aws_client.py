from src.adapter.aws.aws_stepfunctions  import AWSStepFunctions
from src.adapter.aws.aws_logs           import Logs


class AWS:


    def __init__(self):
        self.stepfunctions_client   = AWSStepFunctions()
        self.logs_client            = Logs()
