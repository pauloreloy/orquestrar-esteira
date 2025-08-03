
import json
from src.adapter.aws.aws_config import AWSConfig


class AWSStepFunctions:

    
    def __init__(self):
        self.client = AWSConfig('stepfunctions').get_client()


    def get_state_machine_arn(self, state_machine_name: str):
        response = self.client.list_state_machines()
        for state_machine in response.get('stateMachines', []):
            if state_machine['name'] == state_machine_name:
                return state_machine['stateMachineArn']
        return None


    def start_execution(self, state_machine_name: str, payload: dict):
        state_machine_arn = self.get_state_machine_arn(state_machine_name)
        if not state_machine_arn:
            raise ValueError(f"State machine '{state_machine_name}' not found.")
        response = self.client.start_execution(
            stateMachineArn=state_machine_arn,
            input=json.dumps(payload)
        )
        return response


    def send_task_success(self, task_token: str, payload: dict):
        return self.client.send_task_success(
            taskToken=task_token,
            output=json.dumps(payload)
        )


    def send_task_failure(self, task_token: str, task_error: str, task_error_cause: str):
        return self.client.send_task_failure(
            taskToken=task_token,
            error=str(task_error),
            cause=str(task_error_cause)
        )

