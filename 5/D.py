import sys


class AssertRaises(object):
    def __init__(self, exception_type):
        self.exception_type = exception_type

    def __enter__(self):
        return None

    def __exit__(self, exc_type, exc_val, traceback):
        if isinstance(exc_val, self.exception_type):
            return True
        raise AssertionError

if __name__ == '__main__':
    exec(sys.stdin.read())
