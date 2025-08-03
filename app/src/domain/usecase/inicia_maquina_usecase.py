
from src.adapter.aws.aws_client     import AWS


class IniciaMaquinaUseCase:


    def __init__(self, aws_client: AWS):
        self.aws_client = aws_client


    def execute(self, message: dict):
        _step       = message.get('step')
        _payload    = message.get('payload')
        return self.aws_client.stepfunctions_client.start_execution(_step, _payload)
