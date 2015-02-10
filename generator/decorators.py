from __future__ import print_function, absolute_import


def chain_result(f):
    def wrapped(*args, **kwargs):
        for iterable in f(*args, **kwargs):
            for item in iterable:
                yield item

    return wrapped
