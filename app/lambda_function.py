import json
from src.domain.enums.log_level                     import LogLevel
from src.domain.enums.logger_message                import LoggerMessageEnum
from src.adapter.aws.aws_client                     import AWS
from src.adapter.quickconfig.quickconfig_adapter    import QuickConfigAdapter
from src.domain.usecases.inicia_maquina_usecase     import IniciaMaquinaUseCase
from src.domain.usecases.atualiza_maquina_usecase   import AtualizaMaquinaUseCase
from src.domain.exceptions.usecase_exceptions       import AtualizaMaquinaException
from src.domain.exceptions.usecase_exceptions       import IniciaMaquinaException
from src.common.correlation                         import set_correlation_id


aws_client          = AWS()
quickconfig_adapter = QuickConfigAdapter(aws_client)


def process_sqs_record(record: dict):
    """Processa mensagem recebida via SQS"""
    try:
        message = json.loads(record.get("body", "{}"))
    except (json.JSONDecodeError, TypeError) as e:
        raise RuntimeError(e)

    if message.get("task_token"):
        try:
            AtualizaMaquinaUseCase(aws_client, quickconfig_adapter).execute(message)
        except Exception as e:
            raise AtualizaMaquinaException(e)

    payloads = message.get("payloads")
    if isinstance(payloads, (list, tuple)) and any(payloads):
        for payload in payloads:
            if payload:
                try:
                    IniciaMaquinaUseCase(aws_client, quickconfig_adapter).execute(payload)
                except Exception as e:
                    raise IniciaMaquinaException(e)
    return None


def process_event_record(record: dict):
    if record.get('eventSource') == 'aws:sqs': process_sqs_record(record)


def lambda_handler(event, context):
    set_correlation_id(None)
    aws_client.logs_client.log(
        log_level=LogLevel.INFO,
        log_code=LoggerMessageEnum.L_1000
    )
    for record in event.get('Records', []):
        process_event_record(record)