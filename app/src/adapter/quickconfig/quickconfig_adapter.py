from typing                     import Any
from src.adapter.aws.aws_client import AWS


class QuickConfigAdapter:


    def __init__(self, aws_client: AWS = None):
        self.aws_client = aws_client #pragma: nocover


    def get_value(self, nome_chave: str, valor_padrao: Any):
        return valor_padrao #pragma: nocover
