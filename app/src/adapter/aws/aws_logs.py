import time
import json
import logging
from typing                             import Dict, Any
from src.config                         import params
from src.adapter.aws.aws_config         import AWSConfig
from src.domain.enums.log_level         import LogLevel
from src.domain.enums.logger_message    import LoggerMessageEnum
from src.common.correlation             import get_correlation_id


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
            self.logger.propagate = False
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
            raise RuntimeError(f"Error verifying or creating log group: {e}")


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
            raise RuntimeError(f"Error verifying or creating log stream: {e}")


    def log(self, log_level: LogLevel, log_code: LoggerMessageEnum = None, object: Dict[dict, str] = None) -> None:
        if log_level: self.logger.setLevel(log_level.value)
        try:
            log_entry = {
                "level": str(log_level.value),
                "log_code": log_code.codigo if log_code else None,
                "log_message": log_code.descricao if log_code else None,  
            }
            if get_correlation_id() is not None: log_entry["correlation_id"] = get_correlation_id()
            if object is not None: log_entry["object"] = object
            self.logger.log(
                getattr(logging, str(log_level), logging.INFO),
                json.dumps(log_entry, ensure_ascii=False)
            )
            self.custom_log(log_entry)
        except Exception as e:
            raise RuntimeError(f"Error logging message: {e}")


    def custom_log(self, message: Dict[dict, Any]) -> Any:
        try:
            self.client.put_log_events(
                logGroupName=self.log_group_name,
                logStreamName=self.log_stream_name,
                logEvents=[
                    {
                        'timestamp': int(time.time() * 1000),
                        'message': json.dumps(message)
                    }
                ]
            )
        except Exception as e:
            raise RuntimeError(f"Error logging message: {e}")