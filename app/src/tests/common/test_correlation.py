import unittest
from src.common.correlation import set_correlation_id, get_correlation_id


class TestCorrelation(unittest.TestCase):


    def test_set_and_get_correlation_id(self):
        set_correlation_id("test-id")
        self.assertEqual(get_correlation_id(), "test-id")


    def test_set_correlation_id_none(self):
        set_correlation_id(None)
        self.assertIsNone(get_correlation_id())