
from src.adapter.aws.aws_client     import AWS


class AtualizaMaquinaUseCase:


    def __init__(self, aws_client: AWS):
        self.aws_client = aws_client


    def execute(self, message: dict):
        _payload        = message.get('payload')
        _step_token     = str(message.get('step_token'))
        _step_status    = str(message.get('step_status'))
        if _step_status.lower() == "failure":
            _step_error      = message.get('step_error')
            _step_cause      = message.get('step_cause')
            return self.aws_client.stepfunctions_client.send_task_failure(_step_token, _step_error, _step_cause)
        return self.aws_client.stepfunctions_client.send_task_success(_step_token, _payload)
        
        
        