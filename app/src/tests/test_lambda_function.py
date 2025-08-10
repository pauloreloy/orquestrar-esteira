import unittest
from unittest.mock import patch, MagicMock
from src.adapter.aws.aws_client                     import AWS
from src.adapter.quickconfig.quickconfig_adapter    import QuickConfigAdapter
from src.domain.usecases.inicia_maquina_usecase     import IniciaMaquinaUseCase
from src.domain.usecases.atualiza_maquina_usecase   import AtualizaMaquinaUseCase
from src.domain.exceptions.usecase_exceptions       import AtualizaMaquinaException, IniciaMaquinaException

class TestProcessSQSRecord(unittest.TestCase):

    @patch("src.adapter.aws.aws_logs.AWSConfig")
    def setUp(self, mock_aws_config):
        import lambda_function as lf
        self.lf = lf

    @patch("lambda_function.AtualizaMaquinaUseCase")
    @patch("lambda_function.quickconfig_adapter")
    @patch("lambda_function.aws_client")
    def test_process_sqs_record_with_task_token_success(self, mock_aws_client, mock_quickconfig_adapter, mock_atualiza_uc_cls):
        mock_atualiza_uc = MagicMock()
        mock_atualiza_uc_cls.return_value = mock_atualiza_uc
        mock_atualiza_uc.execute.return_value = "ok"
        record = {"body": '{"task_token": "token", "payload": {"foo": "bar"}}'}
        result = self.lf.process_sqs_record(record)
        mock_atualiza_uc.execute.assert_called_once()
        self.assertIsNone(result)

    @patch("lambda_function.AtualizaMaquinaUseCase")
    @patch("lambda_function.quickconfig_adapter")
    @patch("lambda_function.aws_client")
    def test_process_sqs_record_with_task_token_exception(self, mock_aws_client, mock_quickconfig_adapter, mock_atualiza_uc_cls):
        mock_atualiza_uc = MagicMock()
        mock_atualiza_uc_cls.return_value = mock_atualiza_uc
        mock_atualiza_uc.execute.side_effect = Exception("fail")
        record = {"body": '{"task_token": "token", "payload": {"foo": "bar"}}'}
        with self.assertRaises(AtualizaMaquinaException):
            self.lf.process_sqs_record(record)

    @patch("lambda_function.IniciaMaquinaUseCase")
    @patch("lambda_function.quickconfig_adapter")
    @patch("lambda_function.aws_client")
    def test_process_sqs_record_with_payloads_success(self, mock_aws_client, mock_quickconfig_adapter, mock_inicia_uc_cls):
        mock_inicia_uc = MagicMock()
        mock_inicia_uc_cls.return_value = mock_inicia_uc
        mock_inicia_uc.execute.return_value = "ok"
        record = {"body": '{"payloads": [{"foo": "bar"}, {"baz": "qux"}]}'}
        result = self.lf.process_sqs_record(record)
        self.assertEqual(mock_inicia_uc.execute.call_count, 2)
        self.assertIsNone(result)

    @patch("lambda_function.IniciaMaquinaUseCase")
    @patch("lambda_function.quickconfig_adapter")
    @patch("lambda_function.aws_client")
    def test_process_sqs_record_with_payloads_exception(self, mock_aws_client, mock_quickconfig_adapter, mock_inicia_uc_cls):
        mock_inicia_uc = MagicMock()
        mock_inicia_uc_cls.return_value = mock_inicia_uc
        mock_inicia_uc.execute.side_effect = Exception("fail")
        record = {"body": '{"payloads": [{"foo": "bar"}]}'}
        with self.assertRaises(IniciaMaquinaException):
            self.lf.process_sqs_record(record)

    def test_process_sqs_record_invalid_json(self):
        record = {"body": 'not a json'}
        with self.assertRaises(RuntimeError):
            self.lf.process_sqs_record(record)

    def test_process_sqs_record_empty(self):
        record = {"body": '{}'}
        result = self.lf.process_sqs_record(record)
        self.assertIsNone(result)
