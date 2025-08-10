import unittest
from unittest.mock import MagicMock, patch
from src.domain.strategies.context import Context

class TestContext(unittest.TestCase):


    @patch("src.domain.strategies.context.StepFunction")
    def test_execute_calls_strategy_execute(self, mock_step_function_cls):
        mock_strategy_instance = MagicMock()
        mock_step_function_cls.return_value = mock_strategy_instance
        mock_strategy_instance.execute.return_value = "executed"

        mock_aws_client = MagicMock()
        mock_quickconfig_adapter = MagicMock()
        payload = {"foo": "bar"}

        context = Context("StepFunction", mock_aws_client, mock_quickconfig_adapter)
        result = context.execute(payload)
        self.assertTrue(result)


    @patch("src.domain.strategies.context.StepFunction")
    def test_set_strategy_changes_strategy(self, mock_step_function_cls):
        mock_strategy_instance = MagicMock()
        mock_step_function_cls.return_value = mock_strategy_instance

        context = Context("StepFunction")
        with patch.dict(context.strategies, {"OtherStrategy": MagicMock(return_value=MagicMock())}):
            context.set_strategy("OtherStrategy")
            self.assertEqual(context._strategy_name, "OtherStrategy")
            self.assertTrue(isinstance(context._strategy, MagicMock))


    @patch("src.domain.strategies.context.StepFunction")
    def test_set_strategy_same_strategy_does_not_change(self, mock_step_function_cls):
        mock_strategy_instance = MagicMock()
        mock_step_function_cls.return_value = mock_strategy_instance

        context = Context("StepFunction")
        old_strategy = context._strategy
        context.set_strategy("StepFunction")
        self.assertIs(context._strategy, old_strategy)


    @patch("src.domain.strategies.context.StepFunction")
    def test_init_sets_clients(self, mock_step_function_cls):
        mock_strategy_instance = MagicMock()
        mock_step_function_cls.return_value = mock_strategy_instance

        mock_aws_client = MagicMock()
        mock_quickconfig_adapter = MagicMock()
        context = Context("StepFunction", mock_aws_client, mock_quickconfig_adapter)
        self.assertIs(context.aws_client, mock_aws_client)
        self.assertIs(context.quickconfig_adapter, mock_quickconfig_adapter)