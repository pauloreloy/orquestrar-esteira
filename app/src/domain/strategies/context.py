from src.adapter.aws.aws_client             import AWS


class Context:


    strategies = {}


    def __init__(self, strategy_name: str, aws_client: AWS = None):
        if aws_client: self.aws_client = aws_client
        self._strategy_name = strategy_name
        self._strategy = self.strategies.get(strategy_name)(strategy_name)


    def set_strategy(self, strategy_name: str):
        if strategy_name != self._strategy_name:
            self._strategy = self.strategies.get(strategy_name)
            self._strategy_name = strategy_name


    def execute(self, payload: dict):
        self._strategy.execute(payload, self)