import unittest
from unittest.mock import MagicMock, patch
from src.domain.usecases.inicia_maquina_usecase import IniciaMaquinaUseCase


class TestIniciaMaquinaUseCase(unittest.TestCase):


    @patch("src.domain.usecases.inicia_maquina_usecase.Context")
    def test_execute_calls_context_with_correct_args(self, mock_context_cls):
        mock_aws_client = MagicMock()
        mock_quickconfig_adapter = MagicMock()
        mock_context_instance = MagicMock()
        mock_context_cls.return_value = mock_context_instance
        mock_context_instance.execute.return_value = "result"
        usecase = IniciaMaquinaUseCase(mock_aws_client, mock_quickconfig_adapter)
        payload = {"foo": "bar"}
        result = usecase.execute(payload)
        mock_context_cls.assert_called_once_with("StepFunction", mock_aws_client, mock_quickconfig_adapter)
        mock_context_instance.execute.assert_called_once_with(payload)
        self.assertEqual(result, "result")