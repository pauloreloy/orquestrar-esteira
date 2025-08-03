
import boto3
from src.config import env_config


class AWSConfig:


    def __init__(self, service_name):
        self.service_name           = service_name
        self.endpoint               = env_config.get_aws_endpoint()
        self.region_name            = env_config.get_aws_region()
        self.aws_access_key_id      = env_config.get_aws_access_key_id()
        self.aws_secret_access_key  = env_config.get_aws_access_secret_key()


    def get_client(self):
        return self._create_client()


    def get_resource(self):
        return self._create_resource()


    def _create_client(self):
        client_kwargs = {
            "service_name": self.service_name,
            "region_name":  self.region_name,
        }
        if self.aws_access_key_id and self.aws_secret_access_key:
            client_kwargs["aws_access_key_id"]      = self.aws_access_key_id
            client_kwargs["aws_secret_access_key"]  = self.aws_secret_access_key
        return boto3.client(**client_kwargs)


    def _create_resource(self):
        resource_kwargs = {
            "service_name": self.service_name,
            "region_name":  self.region_name,
        }
        if self.aws_access_key_id and self.aws_secret_access_key:
            resource_kwargs["aws_access_key_id"]        = self.aws_access_key_id
            resource_kwargs["aws_secret_access_key"]    = self.aws_secret_access_key
        return boto3.resource(**resource_kwargs)