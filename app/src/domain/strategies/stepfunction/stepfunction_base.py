from typing import Any
from abc    import ABC, abstractmethod


class StepFunctionsBase(ABC):


    def __init__(self):
        super().__init__()
    

    @abstractmethod
    def execute(self, payload: dict, context: Any = None):
        pass #pragma: nocover



