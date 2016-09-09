import sys
from functools import wraps


def takes(*types):
    def decorator(func):
        @wraps(func)
        def inner(*args, **kwargs):
            for arg, expected_type in zip(args, types):
                if not isinstance(arg, expected_type):
                    raise TypeError
            return func(*args, **kwargs)
        return inner
    return decorator

if __name__ == '__main__':
    exec(sys.stdin.read())
