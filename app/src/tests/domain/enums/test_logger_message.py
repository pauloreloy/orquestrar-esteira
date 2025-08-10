import unittest
from src.domain.enums.logger_message import LoggerMessageEnum

class TestLoggerMessageEnum(unittest.TestCase):


    def test_enum_value(self):
        self.assertEqual(LoggerMessageEnum.L_1000.value, ("L_1000", "Iniciando lambda"))


    def test_enum_attributes(self):
        self.assertEqual(LoggerMessageEnum.L_1000.codigo, "L_1000")
        self.assertEqual(LoggerMessageEnum.L_1000.descricao, "Iniciando lambda")


    def test_str_method(self):
        self.assertEqual(str(LoggerMessageEnum.L_1000), "L_1000: Iniciando lambda")