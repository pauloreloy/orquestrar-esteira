import traceback
from functools                          import wraps
from typing                             import Callable, Optional, Any
from src.adapter.aws.aws_client         import AWS
from src.domain.enums.log_level         import LogLevel
from src.domain.enums.logger_message    import LoggerMessageEnum


def exception_decorator(aws_client: Optional[AWS]) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if aws_client is None and isinstance(args[0].aws_client, AWS):
                    args[0].aws_client.logs_client.log(
                        log_level=LogLevel.ERROR,
                        log_code=LoggerMessageEnum.LAMBDA_ERROR,
                        message={
                            "message": str(e),
                            "function": func.__name__,
                            "*args **kwargs": str(f"{args, kwargs}"),
                            "traceback": str(traceback.format_exc())
                        }
                    )
                else:
                    aws_client.logs_client.log(
                        log_level=LogLevel.ERROR,
                        log_code=LoggerMessageEnum.LAMBDA_ERROR,
                        message={
                            "message": str(e),
                            "function": func.__name__,
                            "*args **kwargs": str(f"{args, kwargs}"),
                            "traceback": str(traceback.format_exc())
                        }
                    )
                raise e.__class__(e)
        return wrapper
    return decorator
