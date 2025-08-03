
from src.adapter.aws.aws_sqs            import AWSSQS
from src.adapter.aws.aws_s3             import S3
from src.adapter.aws.aws_stepfunctions  import AWSStepFunctions


class AWS:


    def __init__(self):
        self.stepfunctions_client   = AWSStepFunctions()
