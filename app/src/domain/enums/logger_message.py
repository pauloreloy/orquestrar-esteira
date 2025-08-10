import enum


class LoggerMessageEnum(enum.Enum):

    L_1000 = ("L_1000", "Iniciando lambda")


    def __init__(self, codigo: str, descricao: str):
        self.codigo = codigo
        self.descricao = descricao


    def __str__(self):
        return f"{self.codigo}: {self.descricao}"