class AtualizaMaquinaException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


class IniciaMaquinaException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

