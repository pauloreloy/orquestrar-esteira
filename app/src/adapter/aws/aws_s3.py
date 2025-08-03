
from src.adapter.aws.aws_config import AWSConfig


class S3:

    
    def __init__(self):
        self.client = AWSConfig("s3").get_client()


    def list_buckets(self):
        response = self.client.list_buckets()
        return response.get('Buckets', [])