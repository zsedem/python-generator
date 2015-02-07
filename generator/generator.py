from __future__ import absolute_import, print_function
import itertools


class GeneratorIteratedTwice(Exception):
    pass


class Generator(object):
    def __init__(self, generator):
        self._source_generator = generator
        self._iterate_finished = False
        self._count_iter = 0
        self._data_collectors = []

    def __call_data_collectors(self, result):
        for data_collector in self._data_collectors:
            data_collector.collect(result)

    def __next__(self):
        try:
            result = next(self._source_generator)
            self._count_iter += 1
            self.__call_data_collectors(result)
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

    def add_data_collector(self, data_collector):
        self._data_collectors.append(data_collector)

    def is_finished(self):
        return self._iterate_finished
