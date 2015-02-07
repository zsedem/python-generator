from __future__ import absolute_import, print_function
from ..datacollector import DataCollector, NonCallableError
import unittest


class TestDataCollector(unittest.TestCase):
    def test_init_method_raises_error_on_not_callable_argument(self):
        with self.assertRaises(NonCallableError):
            DataCollector(4, None)

    def test_collect_calls_added_the_method(self):
        data_collector = DataCollector(lambda result, value: result + [value], [])
        data_collector.collect(5)
        self.assertEqual(data_collector.get_collected_data(), [5])

    def test_collect_data_can_call_foreign_method(self):
        test_result = []
        data_collector = DataCollector(lambda _, value: test_result.append(value), None)
        data_collector.collect(2)
        self.assertEqual(test_result, [2])
