import json
from src.domain.enum.loglevel                       import LogLevel
from src.adapter.aws.aws_client                     import AWS
from src.domain.usecase.inicia_maquina_usecase      import IniciaMaquinaUseCase
from src.domain.usecase.atualiza_maquina_usecase    import AtualizaMaquinaUseCase


aws_client = AWS()


def process_sqs_record(record: dict):
    message = json.loads(record.get('body'))
    if message.get('step_token'):
        AtualizaMaquinaUseCase(aws_client).execute(message)
    if message.get('step') and not message.get('step_token'):
        IniciaMaquinaUseCase(aws_client).execute(message)


def process_event_record(record: dict):
    if record.get('eventSource') == 'aws:sqs': process_sqs_record(record)


def lambda_handler(event, context):
    aws_client.logs_client.custom_log(
        log_level=LogLevel.INFO,
        message="Lambda function started processing event"
    )
    for record in event.get('Records', []):
        process_event_record(record)