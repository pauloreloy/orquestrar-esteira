import unittest
from unittest.mock                      import patch, MagicMock
from src.adapter.aws.aws_stepfunctions  import StepFunctions


class TestAWSStepFunctions(unittest.TestCase):


    def setUp(self):
        patcher = patch("src.adapter.aws.aws_stepfunctions.AWSConfig")
        self.addCleanup(patcher.stop)
        self.mock_config = patcher.start()
        self.mock_client = MagicMock()
        self.mock_config.return_value.get_client.return_value = self.mock_client
        self.stepfunctions = StepFunctions()


    def test_get_state_machine_arn_found(self):
        self.mock_client.list_state_machines.return_value = {
            "stateMachines": [
                {"name": "my_machine", "stateMachineArn": "arn:aws:states:region:123:stateMachine:my_machine"}
            ]
        }
        arn = self.stepfunctions.get_state_machine_arn("my_machine")
        self.assertEqual(arn, "arn:aws:states:region:123:stateMachine:my_machine")


    def test_get_state_machine_arn_not_found(self):
        self.mock_client.list_state_machines.return_value = {"stateMachines": []}
        arn = self.stepfunctions.get_state_machine_arn("unknown_machine")
        self.assertIsNone(arn)


    def test_start_execution_success(self):
        state_machine_name = "test_machine"
        payload = {"key": "value"}
        arn = "arn:aws:states:region:123456789012:stateMachine:test_machine"
        self.mock_client.list_state_machines.return_value = {
            "stateMachines": [{"name": state_machine_name, "stateMachineArn": arn}]
        }
        self.mock_client.start_execution.return_value = {"executionArn": "exec-arn"}
        result = self.stepfunctions.start_execution(state_machine_name, payload)
        self.assertEqual(result, {"executionArn": "exec-arn"})
        self.mock_client.start_execution.assert_called_once()
        args, kwargs = self.mock_client.start_execution.call_args
        self.assertEqual(kwargs["stateMachineArn"], arn)


    def test_start_execution_state_machine_not_found(self):
        state_machine_name = "missing_machine"
        payload = {"key": "value"}
        self.mock_client.list_state_machines.return_value = {"stateMachines": []}
        with self.assertRaises(ValueError) as excinfo:
            self.stepfunctions.start_execution(state_machine_name, payload)
        self.assertIn("State machine 'missing_machine' not found.", str(excinfo.exception))


    def test_start_execution_runtime_error(self):
        state_machine_name = "test_machine"
        payload = {"key": "value"}
        arn = "arn:aws:states:region:123456789012:stateMachine:test_machine"
        self.mock_client.list_state_machines.return_value = {
            "stateMachines": [{"name": state_machine_name, "stateMachineArn": arn}]
        }
        self.mock_client.start_execution.side_effect = Exception("AWS error")
        with self.assertRaises(RuntimeError) as excinfo:
            self.stepfunctions.start_execution(state_machine_name, payload)
        self.assertIn("AWS error", str(excinfo.exception))


    def test_send_task_success(self):
        self.mock_client.send_task_success.return_value = {"status": "success"}
        result = self.stepfunctions.send_task_success("token123", {"foo": "bar"})
        self.assertEqual(result, {"status": "success"})
        self.mock_client.send_task_success.assert_called_once()
        args, kwargs = self.mock_client.send_task_success.call_args
        self.assertEqual(kwargs["taskToken"], "token123")
        self.assertIn('"foo": "bar"', kwargs["output"])


    def test_send_task_failure(self):
        self.mock_client.send_task_failure.return_value = {"status": "failed"}
        result = self.stepfunctions.send_task_failure("token456", "error", "cause")
        self.assertEqual(result, {"status": "failed"})
        self.mock_client.send_task_failure.assert_called_once()
        args, kwargs = self.mock_client.send_task_failure.call_args
        self.assertEqual(kwargs["taskToken"], "token456")
        self.assertEqual(kwargs["error"], "error")
        self.assertEqual(kwargs["cause"], "cause")