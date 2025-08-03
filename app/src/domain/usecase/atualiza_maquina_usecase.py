
from src.adapter.aws.aws_client     import AWS


class AtualizaMaquinaUseCase:


    def __init__(self, aws_client: AWS):
        self.aws_client = aws_client


    def execute(self, message: dict):
        _payload        = message.get('payload')
        _task_token     = str(message.get('task_token'))
        _task_status    = str(message.get('task_status'))
        if _task_status.lower() == "failure":
            _task_error         = message.get('task_error')
            _task_error_cause   = message.get('task_error_cause')
            return self.aws_client.stepfunctions_client.send_task_failure(_task_token, _task_error, _task_error_cause)
        return self.aws_client.stepfunctions_client.send_task_success(_task_token, _payload)
        
        
        