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
from src.domain.decorators.exception                import exception_decorator


aws_client          = AWS()
quickconfig_adapter = QuickConfigAdapter(aws_client)


def process_sqs_record(record: dict):
    """Processa mensagem recebida via SQS"""
    try:
        message = json.loads(record.get("body", "{}"))
    except (json.JSONDecodeError, TypeError) as e:
        raise RuntimeError(e)
    if message.get("correlation_id"): set_correlation_id(message.get("correlation_id"))
    payloads = message.get("payloads")
    if isinstance(payloads, (list, tuple)) and any(payloads):
        for payload in payloads:
            if payload:
                try:
                    @exception_decorator(aws_client)
                    def inicia_maquina(payload):
                        IniciaMaquinaUseCase(aws_client, quickconfig_adapter).execute(payload)
                    inicia_maquina(payload)
                except Exception as e:
                    raise IniciaMaquinaException(e)
    return None


def process_event_record(record: dict):
    if record.get('eventSource') == 'aws:sqs': process_sqs_record(record)


def process_task_token(event: dict):
    if event.get("correlation_id"): set_correlation_id(event.get("correlation_id"))
    if event.get("task_token"):
        try:
            @exception_decorator(aws_client)
            def atualiza_maquina(message):
                return AtualizaMaquinaUseCase(aws_client, quickconfig_adapter).execute(message)
            atualiza_maquina(event)
        except Exception as e:
            raise AtualizaMaquinaException(e)


def lambda_handler(event, context):
    print(event)
    set_correlation_id(None)
    aws_client.logs_client.log(
        log_level=LogLevel.INFO,
        log_code=LoggerMessageEnum.L_1000
    )
    if event.get("task_token"):
        return process_task_token(event)
    for record in event.get('Records', []):
        process_event_record(record)