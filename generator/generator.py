from __future__ import absolute_import, print_function
import itertools


class GeneratorNotRestartable(Exception):
    pass


class GeneratorIteratedTwice(Exception):
    pass


class Generator(object):
    def __init__(self, generator, iterator_restarter=None):
        self._mapping_functions = []
        self._original_iterable_object = generator
        self._iterator_restarter = iterator_restarter
        self._callbacks = []
        self._initialize_generator()

    def _initialize_generator(self):
        self._source_generator = iter(self._original_iterable_object)
        self._iterate_finished = False
        self._count_iter = 0

    def __call_callbacks(self, result):
        for callback in self._callbacks:
            callback(result)

    def __next__(self):
        try:
            result = next(self._source_generator)
            result = self.__call_mappings(result)
            self._count_iter += 1
            self.__call_callbacks(result)
            return result
        except StopIteration:
            if not self._iterate_finished:
                self._iterate_finished = True
                raise
            else:
                raise GeneratorIteratedTwice("This usually means, that you use the generator wrong")
    next = __next__

    def __iter__(self):
        return self

    def iter_chunks(self, chunk_size):
        if self._iterate_finished:
            raise GeneratorIteratedTwice("This usually means, that you use the generator wrong")

        chunk = self.__get_chunk(chunk_size)
        while not self._iterate_finished:
            yield chunk
            while self._count_iter % chunk_size != 0 and not self._iterate_finished:
                next(self)

            chunk = self.__get_chunk(chunk_size)

    def __get_chunk(self, chunk_size):
        try:
            first = next(self)
        except (StopIteration, GeneratorIteratedTwice):
            return None
        return itertools.chain([first], self.__take(chunk_size - 1))

    def __take(self, count):
        for _ in range(count):
            yield next(self)

    def add_callback(self, callback):
        self._callbacks.append(callback)

    def add_data_collector(self, data_collector):
        self._callbacks.append(data_collector.collect)

    def is_finished(self):
        return self._iterate_finished

    def reset(self):
        if self._iterator_restarter is None:
            raise GeneratorNotRestartable("No generator restart function provided for the source object")
        self._iterator_restarter(self._original_iterable_object)
        self._initialize_generator()

    def map(self, function):
        self._mapping_functions.append(function)
        return self

    def __call_mappings(self, result):
        for func in self._mapping_functions:
            result = func(result)
        return result
