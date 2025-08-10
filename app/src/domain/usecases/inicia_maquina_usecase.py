
from src.adapter.aws.aws_client                     import AWS
from src.domain.strategies.context                  import Context
from src.adapter.quickconfig.quickconfig_adapter    import QuickConfigAdapter


class IniciaMaquinaUseCase:


    def __init__(self, aws_client: AWS, quickconfig_adapter: QuickConfigAdapter):
        self.aws_client             = aws_client
        self.quickconfig_adapter    = quickconfig_adapter


    def execute(self, payload: dict):
        context = Context("StepFunction", self.aws_client, self.quickconfig_adapter)
        return context.execute(payload)
