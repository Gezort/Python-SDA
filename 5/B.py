import sys
from functools import wraps


class Generator(object):
    def __init__(self, gen, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.generator = gen(*args, **kwargs)
        self.generator_function = gen

    def __next__(self):
        try:
            return next(self.generator)
        except StopIteration:
            self.generator = self.generator_function(*self.args, **self.kwargs)
            raise StopIteration

    def __iter__(self):
        return self

    def __call__(self):
        return self


def inexhaustible(gen):
    @wraps(gen)
    def inner(*args, **kwargs):
        return Generator(gen, *args, **kwargs)
    return inner


@inexhaustible
def gen():
    yield 1
    yield 2


if __name__ == '__main__':
    exec(sys.stdin.read())
