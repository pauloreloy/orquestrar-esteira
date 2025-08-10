from src.adapter.aws.aws_client                             import AWS
from src.adapter.quickconfig.quickconfig_adapter            import QuickConfigAdapter
from src.domain.strategies.stepfunction.step_function       import StepFunction


class Context:


    strategies = {
        "StepFunction":    StepFunction 
    }


    def __init__(self, strategy_name: str, aws_client: AWS = None, quickconfig_adapter: QuickConfigAdapter = None):
        if aws_client: self.aws_client                      = aws_client
        if quickconfig_adapter: self.quickconfig_adapter    = quickconfig_adapter
        self._strategy_name                                 = strategy_name
        self._strategy                                      = self.strategies.get(strategy_name)()


    def set_strategy(self, strategy_name: str):
        if strategy_name        != self._strategy_name:
            self._strategy      = self.strategies.get(strategy_name)
            self._strategy_name = strategy_name


    def execute(self, payload: dict):
        return self._strategy.execute(payload, self)