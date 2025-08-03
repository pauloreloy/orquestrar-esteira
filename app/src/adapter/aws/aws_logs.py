import time
import json
import logging
from src.config                 import params
from src.adapter.aws.aws_config import AWSConfig
from src.domain.enum.loglevel   import LogLevel


class Logs:

    
    def __init__(self, log_group_name: str = params.LAMBDA_LOG_GROUP, log_stream_name: str = params.LAMBDA_NAME):
        self.client             = AWSConfig("logs").get_client()
        self.log_group_name     = log_group_name
        self.log_stream_name    = log_stream_name
        self.logger             = logging.getLogger(params.LAMBDA_NAME)
        if not self.logger.handlers:
            handler     = logging.StreamHandler()
            formatter   = logging.Formatter('%(asctime)s %(levelname)s %(name)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        self.verify_log_group()
        self.verify_log_stream()


    def verify_log_group(self):
        try:
            response = self.client.describe_log_groups(logGroupNamePrefix=self.log_group_name)
            exists = any(group['logGroupName'] == self.log_group_name for group in response.get('logGroups', []))
            if not exists:
                self.client.create_log_group(logGroupName=self.log_group_name)
                return True
            return True
        except Exception as e:
            print(f"Error verifying or creating log group: {e}")
            return False


    def verify_log_stream(self):
        try:
            response = self.client.describe_log_streams(
                logGroupName=self.log_group_name,
                logStreamNamePrefix=self.log_stream_name
            )
            exists = any(stream['logStreamName'] == self.log_stream_name for stream in response.get('logStreams', []))
            if not exists:
                self.client.create_log_stream(
                    logGroupName=self.log_group_name,
                    logStreamName=self.log_stream_name
                )
                return True
            return True
        except Exception as e:
            print(f"Error verifying or creating log stream: {e}")
            return False
        

    def custom_log(self, log_level: LogLevel, message: str):
        self.logger.setLevel(log_level.value)
        try:
            log_entry = {
                "level": str(log_level),
                "lambda": params.LAMBDA_NAME,
                "message": message
            }
            self.logger.log(
                getattr(logging, str(log_level), logging.INFO),
                json.dumps(message, ensure_ascii=False, indent=4) if isinstance(message, dict) else message
            )
            self.client.put_log_events(
                logGroupName=self.log_group_name,
                logStreamName=self.log_stream_name,
                logEvents=[
                    {
                        'timestamp': int(time.time() * 1000),
                        'message': json.dumps(log_entry)
                    }
                ]
            )
        except Exception as e:
            print(f"Error logging message: {e}")