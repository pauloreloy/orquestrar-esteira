import unittest
import json
from unittest.mock import patch
import importlib

class TestCase1(unittest.TestCase):

    def setUp(self):
        self.patcher = patch("src.adapter.aws.aws_client.AWS")
        self.mock_aws = self.patcher.start()
        import lambda_function
        importlib.reload(lambda_function)
        self.lf = lambda_function

    def tearDown(self):
        self.patcher.stop()

    def test_case_1(self):
        with open("src/tests/payloads/event_valida_retido.json") as f:
            event = json.loads(f.read())
        self.lf.lambda_handler(event, None)