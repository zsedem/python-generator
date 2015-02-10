from __future__ import print_function, absolute_import
import unittest
from .. import chain_result


class TestDecorators(unittest.TestCase):
    def test_chain_result_works_for_empty_generator(self):
        self.assertEqual(
            list(
                chain_result(lambda: iter([]))()
            ),
            [])

    def test_chain_result_should_give_back_chained_result(self):
        result = list(chain_result(lambda: [[1], [2], [3]])())
        self.assertEqual(result, [1, 2, 3])
