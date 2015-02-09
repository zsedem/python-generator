from __future__ import absolute_import, print_function
from .. import Generator, GeneratorIteratedTwice, DataCollector, GeneratorNotRestartable
import unittest


class TestGenerator(unittest.TestCase):
    def test_generator_returns_generator(self):
        generator = Generator(iter([1, 2, 3, 4]))
        self.assertEqual(generator.next(), 1)
        self.assertEqual(list(generator), [2, 3, 4])

    def test_generator_raise_error_if_tried_to_iterate_two_times(self):
        generator = Generator(iter([1, 2, 3, 4]))
        list(generator)
        with self.assertRaises(GeneratorIteratedTwice):
            list(generator)

    def test_generator_iter_slices_method_should_give_empty_list_for_empty(self):
        data = Generator(iter([]))
        self.assertEqual([list(chunk) for chunk in data.iter_chunks(2)],
                         [])

    def test_generator_iter_slices_method_give_back_the_chunks(self):
        data = Generator(iter([1, 2, 3, 4, 5]))
        self.assertEqual([list(chunk) for chunk in data.iter_chunks(2)],
                         [[1, 2], [3, 4], [5]])

    def test_generator_iter_slices_give_back_same_number_of_slices_even_if_we_do_not_iterate_on_the_slices(self):
        data = Generator(iter([1, 2, 3, 4, 5]))
        l = list(data.iter_chunks(2))
        self.assertEqual(len(l), 3, '{} length is not 3'.format(l))
        with self.assertRaises(GeneratorIteratedTwice):
            list(data.iter_chunks(2))

    def test_generator_iteration_finished_returns_right(self):
        generator = Generator(iter([1]))
        self.assertFalse(generator.is_finished())
        self._iterate_to_end(generator)
        self.assertTrue(generator.is_finished())

    def test_generator_collects_data_with_registered_collector(self):
        generator = Generator(iter([1, 2, 3, 4, 5]))
        summing = DataCollector(lambda x, y: x + y, 0)
        generator.add_data_collector(summing)
        self._iterate_to_end(generator)
        self.assertEqual(summing.get_collected_data(), sum([1, 2, 3, 4, 5]))

    def test_generator_can_be_reitered_if_reset_function_provided(self):
        generator = Generator([1, 2, 3], iterator_restarter=id)
        self.assertEqual(list(generator), [1, 2, 3])
        self.assertTrue(generator.is_finished())
        generator.reset()
        self.assertEqual(list(generator), [1, 2, 3])
        self.assertTrue(generator.is_finished())

    def test_generator_reset_raise_exception_if_there_was_no_restarter_method_defined(self):
        generator = Generator([1, 2, 3])
        with self.assertRaises(GeneratorNotRestartable):
            generator.reset()

    def test_generator_map_method_returns_generator_too(self):
        generator = Generator([1, 2, 3, 4]).map(lambda x: x % 2 == 0)
        self.assertIsInstance(generator, Generator)
        self.assertEqual(list(generator), [False, True, False, True])

    def test_generator_calls_callback_functions(self):
        generator = Generator([1, 2, 3, 4])
        callback_args = []
        generator.add_callback(callback_args.append)
        self._iterate_to_end(generator)
        self.assertEqual(callback_args, [1, 2, 3, 4])

    def _iterate_to_end(self, generator):
        for _ in generator:
            pass
