import unittest
from src.config                         import params
from unittest.mock                      import patch, MagicMock
from src.adapter.aws.aws_logs           import Logs
from src.domain.enums.log_level         import LogLevel
from src.domain.enums.logger_message    import LoggerMessageEnum


class TestAWSLogs(unittest.TestCase):


    def setUp(self):
        aws_config_patch = patch("src.adapter.aws.aws_logs.AWSConfig")
        self.addCleanup(aws_config_patch.stop)
        self.mock_config = aws_config_patch.start()


    @patch("src.adapter.aws.aws_logs.AWSConfig")
    @patch("src.adapter.aws.aws_logs.logging.getLogger")
    def test_init_creates_logger_and_verifies_group_and_stream(self, mock_get_logger, mock_aws_config):
        mock_client = MagicMock()
        mock_aws_config.return_value.get_client.return_value = mock_client
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        mock_logger.handlers = []
        with patch.object(Logs, "verify_log_group") as mock_verify_group, \
             patch.object(Logs, "verify_log_stream") as mock_verify_stream:
            mock_verify_group.return_value = True
            mock_verify_stream.return_value = True
            logs = Logs("test-group", "test-stream")
            mock_aws_config.assert_called_once_with("logs")
            mock_get_logger.assert_called_once()
            self.assertEqual(logs.log_group_name, "test-group")
            self.assertEqual(logs.log_stream_name, "test-stream")
            mock_verify_group.assert_called_once()
            mock_verify_stream.assert_called_once()
            self.assertIs(logs.logger, mock_logger)
            self.assertIs(logs.client, mock_client)

    @patch("src.adapter.aws.aws_logs.AWSConfig")
    @patch("src.adapter.aws.aws_logs.logging.getLogger")
    def test_init_logger_already_has_handlers(self, mock_get_logger, mock_aws_config):
        mock_client = MagicMock()
        mock_aws_config.return_value.get_client.return_value = mock_client
        mock_logger = MagicMock()
        mock_logger.handlers = [MagicMock()]
        mock_get_logger.return_value = mock_logger
        with patch.object(Logs, "verify_log_group") as mock_verify_group, \
             patch.object(Logs, "verify_log_stream") as mock_verify_stream:
            logs = Logs("group", "stream")
            self.assertEqual(len(mock_logger.handlers), 1)
            mock_verify_group.assert_called_once()
            mock_verify_stream.assert_called_once()

    
    def test_verify_log_group(self):
        self.mock_client = MagicMock()
        self.mock_config.return_value.get_client.return_value = self.mock_client
        self.mock_client.describe_log_groups.return_value = {
            "logGroups": [
                {
                "logGroupName": params.LAMBDA_LOG_GROUP
                }
            ]
        }
        logs = Logs()
        self.assertTrue(logs.verify_log_group())
        self.mock_client.describe_log_groups.return_value = {}
        self.assertTrue(logs.verify_log_group())
    

    def test_verify_log_group_exception(self):
        self.mock_client = MagicMock()
        self.mock_config.return_value.get_client.return_value = self.mock_client
        self.mock_client.describe_log_groups.side_effect = Exception
        with self.assertRaises(Exception):
            Logs().verify_log_group()


    def test_verify_log_stream(self):
        self.mock_client = MagicMock()
        self.mock_config.return_value.get_client.return_value = self.mock_client
        self.mock_client.describe_log_streams.return_value = {
            "logStreams": [
                {
                "logStreamName": params.LAMBDA_NAME
                }
            ]
        }
        logs = Logs()
        self.assertTrue(logs.verify_log_stream())
        self.mock_client.describe_log_streams.return_value = {}
        self.assertTrue(logs.verify_log_stream())
    
    
    def test_verify_log_strem_exception(self):
        self.mock_client = MagicMock()
        self.mock_config.return_value.get_client.return_value = self.mock_client
        self.mock_client.describe_log_streams.side_effect = Exception
        with self.assertRaises(Exception):
            Logs().verify_log_stream()

    
    def test_log(self):
        self.mock_client = MagicMock()
        self.mock_config.return_value.get_client.return_value = self.mock_client
        logs = Logs()
        logs.log(
            log_level=LogLevel.INFO,
            log_code=LoggerMessageEnum.L_1000,
            object={"key": "value"}
        )
    

    def test_log_exception(self):
        self.mock_client = MagicMock()
        self.mock_config.return_value.get_client.return_value = self.mock_client
        logs = Logs()
        with patch.object(logs.logger, 'log', side_effect=Exception("Logging error")):
            with self.assertRaises(Exception):
                logs.log(
                    log_level=LogLevel.INFO,
                    log_code=LoggerMessageEnum.L_1000,
                    object={"key": "value"}
                )
    

    def test_custom_log_exception(self):
        self.mock_client = MagicMock()
        self.mock_config.return_value.get_client.return_value = self.mock_client
        self.mock_client.put_log_events.side_effect = Exception
        logs = Logs()
        with self.assertRaises(Exception):
            logs.custom_log({"message": "test"})