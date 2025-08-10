import unittest
from src.domain.enums.log_level import LogLevel


class TestLogLevel(unittest.TestCase):


    def test_enum_values(self):
        self.assertEqual(LogLevel.DEBUG.value, "DEBUG")
        self.assertEqual(LogLevel.INFO.value, "INFO")
        self.assertEqual(LogLevel.WARNING.value, "WARNING")
        self.assertEqual(LogLevel.ERROR.value, "ERROR")
        self.assertEqual(LogLevel.CRITICAL.value, "CRITICAL")


    def test_str_method(self):
        self.assertEqual(str(LogLevel.DEBUG), "DEBUG")
        self.assertEqual(str(LogLevel.INFO), "INFO")
        self.assertEqual(str(LogLevel.WARNING), "WARNING")
        self.assertEqual(str(LogLevel.ERROR), "ERROR")
        self.assertEqual(str(LogLevel.CRITICAL), "CRITICAL")


    def test_from_str_valid(self):
        self.assertEqual(LogLevel.from_str("debug"), LogLevel.DEBUG)
        self.assertEqual(LogLevel.from_str("INFO"), LogLevel.INFO)
        self.assertEqual(LogLevel.from_str("Warning"), LogLevel.WARNING)
        self.assertEqual(LogLevel.from_str("error"), LogLevel.ERROR)
        self.assertEqual(LogLevel.from_str("CRITICAL"), LogLevel.CRITICAL)


    def test_from_str_invalid(self):
        with self.assertRaises(ValueError) as cm:
            LogLevel.from_str("notalevel")
        self.assertEqual(str(cm.exception), "Invalid log level: notalevel")