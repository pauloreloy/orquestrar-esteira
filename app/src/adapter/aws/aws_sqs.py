
from src.adapter.aws.aws_config import AWSConfig


class AWSSQS:

    
    def __init__(self):
        self.client = AWSConfig('sqs').get_client()


    def send_message(self, queue_url, message_body):
        response = self.client.send_message(
            QueueUrl=queue_url,
            MessageBody=message_body
        )
        return response


    def receive_messages(self, queue_url, max_number_of_messages=1):
        response = self.client.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=max_number_of_messages
        )
        return response.get('Messages', [])