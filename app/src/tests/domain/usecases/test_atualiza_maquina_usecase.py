import unittest
from unittest.mock import MagicMock
from src.domain.usecases.atualiza_maquina_usecase import AtualizaMaquinaUseCase


class TestAtualizaMaquinaUseCase(unittest.TestCase):


    def setUp(self):
        self.mock_aws_client = MagicMock()
        self.mock_stepfunctions_client = MagicMock()
        self.mock_aws_client.stepfunctions_client = self.mock_stepfunctions_client
        self.mock_quickconfig_adapter = MagicMock()
        self.usecase = AtualizaMaquinaUseCase(self.mock_aws_client, self.mock_quickconfig_adapter)


    def test_execute_success(self):
        message = {
            'payload': {'foo': 'bar'},
            'task_token': 'token123'
        }
        self.mock_stepfunctions_client.send_task_success.return_value = 'success'
        result = self.usecase.execute(message)
        self.mock_stepfunctions_client.send_task_success.assert_called_once_with(
            'token123', {'Payload': {'foo': 'bar'}}
        )
        self.assertEqual(result, 'success')


    def test_execute_failure(self):
        message = {
            'payload': {'foo': 'bar'},
            'task_token': 'token123',
            'task_error': 'error',
            'task_error_cause': 'cause'
        }
        self.mock_stepfunctions_client.send_task_failure.return_value = 'failure'
        result = self.usecase.execute(message)
        self.mock_stepfunctions_client.send_task_failure.assert_called_once_with(
            'token123', 'error', 'cause'
        )
        self.assertEqual(result, 'failure')