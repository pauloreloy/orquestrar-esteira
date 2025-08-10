import unittest
from unittest.mock import patch, MagicMock
from src.adapter.aws.aws_client import AWS


class TestAWS(unittest.TestCase):


    @patch("src.adapter.aws.aws_client.StepFunctions")
    @patch("src.adapter.aws.aws_client.Logs")
    def test_init_creates_clients(self, mock_logs, mock_stepfunctions):
        mock_sf_instance = MagicMock()
        mock_logs_instance = MagicMock()
        mock_stepfunctions.return_value = mock_sf_instance
        mock_logs.return_value = mock_logs_instance

        aws = AWS()
        mock_stepfunctions.assert_called_once_with()
        mock_logs.assert_called_once_with()
        self.assertIs(aws.stepfunctions_client, mock_sf_instance)
        self.assertIs(aws.logs_client, mock_logs_instance)
