from __future__ import print_function, absolute_import


class NonCallableError(TypeError):
    pass


class DataCollector(object):
    def __init__(self, collector_func, zero_value):
        self._collector_func = collector_func
        self._reduce_result = zero_value
        if not callable(self._collector_func):
            raise NonCallableError("{} type is not callable".format(type(self._collector_func)))

    def collect(self, value):
        self._reduce_result = self._collector_func(self._reduce_result, value)

    def get_collected_data(self):
        return self._reduce_result
