import os
from src.config import params


def get_aws_endpoint():
    return os.getenv('AWS_ENDPOINT', params.AWS_ENDPOINT)


def get_aws_region():
    return os.getenv('AWS_REGION', params.AWS_REGION)


def get_aws_access_key_id():
    return os.getenv('AWS_ACCESS_KEY_ID', params.AWS_ACCESS_KEY_ID)


def get_aws_access_secret_key():
    return os.getenv('AWS_ACCESS_SECRET_KEY', params.AWS_ACCESS_SECRET_KEY)