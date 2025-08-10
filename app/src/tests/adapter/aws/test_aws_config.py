import unittest
from unittest.mock import patch, MagicMock
from src.adapter.aws.aws_config import AWSConfig


class TestAWSConfig(unittest.TestCase):

    def setUp(self):
        boto_patch = patch("src.adapter.aws.aws_config.boto3")
        self.addCleanup(boto_patch.stop)
        self.mock_boto = boto_patch.start()

    @patch("src.adapter.aws.aws_config.env_config")
    def test_init_sets_attributes(self, mock_env_config):
        mock_env_config.get_aws_endpoint.return_value = "http://localhost:4566"
        mock_env_config.get_aws_region.return_value = "us-east-1"
        mock_env_config.get_aws_access_key_id.return_value = "fake_access_key"
        mock_env_config.get_aws_access_secret_key.return_value = "fake_secret_key"
        config = AWSConfig("s3")
        self.assertEqual(config.service_name, "s3")
        self.assertEqual(config.endpoint, "http://localhost:4566")
        self.assertEqual(config.region_name, "us-east-1")
        self.assertEqual(config.aws_access_key_id, "fake_access_key")
        self.assertEqual(config.aws_secret_access_key, "fake_secret_key")


    @patch("src.adapter.aws.aws_config.env_config")
    def test_init_with_missing_keys(self, mock_env_config):
        mock_env_config.get_aws_endpoint.return_value = None
        mock_env_config.get_aws_region.return_value = "us-west-2"
        mock_env_config.get_aws_access_key_id.return_value = None
        mock_env_config.get_aws_access_secret_key.return_value = None
        config = AWSConfig("dynamodb")
        self.assertEqual(config.service_name, "dynamodb")
        self.assertIsNone(config.endpoint)
        self.assertEqual(config.region_name, "us-west-2")
        self.assertIsNone(config.aws_access_key_id)
        self.assertIsNone(config.aws_secret_access_key)


    def test_create_client(self):
        mock_boto_client = MagicMock()
        self.mock_boto.client.return_value = mock_boto_client
        config = AWSConfig("s3")
        client = config._create_client()
        self.assertIs(client, mock_boto_client)
    
    
    def test_create_client_with_keys(self):
        with patch("src.adapter.aws.aws_config.env_config") as mock_env_config:
            mock_env_config.get_aws_access_key_id.return_value = "fake_access_key"
            mock_env_config.get_aws_access_secret_key.return_value = "fake_secret_key"
            mock_boto_client = MagicMock()
            self.mock_boto.client.return_value = mock_boto_client
            config = AWSConfig("s3")
            client = config._create_client()
            self.assertIs(client, mock_boto_client)
            client = config.get_client()
            self.assertIs(client, mock_boto_client)


    def test_create_resource(self):
        mock_boto_client = MagicMock()
        self.mock_boto.resource.return_value = mock_boto_client
        config = AWSConfig("s3")
        client = config._create_resource()
        self.assertIs(client, mock_boto_client)


    def test_create_resource_with_keys(self):
        with patch("src.adapter.aws.aws_config.env_config") as mock_env_config:
            mock_env_config.get_aws_access_key_id.return_value = "fake_access_key"
            mock_env_config.get_aws_access_secret_key.return_value = "fake_secret_key"
            mock_boto_client = MagicMock()
            self.mock_boto.resource.return_value = mock_boto_client
            config = AWSConfig("s3")
            client = config._create_resource()
            self.assertIs(client, mock_boto_client)
            resource = config.get_resource()
            self.assertIs(resource, mock_boto_client)
