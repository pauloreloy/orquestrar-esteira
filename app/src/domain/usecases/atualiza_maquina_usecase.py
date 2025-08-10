
from src.adapter.aws.aws_client                     import AWS
from src.adapter.quickconfig.quickconfig_adapter    import QuickConfigAdapter


class AtualizaMaquinaUseCase:


    def __init__(self, aws_client: AWS, quickconfig_adapter: QuickConfigAdapter):
        self.aws_client             = aws_client
        self.quickconfig_adapter    = quickconfig_adapter


    def execute(self, message: dict):
        _payload        = {
            "Payload": message.get('payload')
        }
        _task_token     = str(message.get('task_token'))
        if message.get('task_error'):
            _task_error         = message.get('task_error')
            _task_error_cause   = message.get('task_error_cause')
            return self.aws_client.stepfunctions_client.send_task_failure(_task_token, _task_error, _task_error_cause)
        return self.aws_client.stepfunctions_client.send_task_success(_task_token, _payload)