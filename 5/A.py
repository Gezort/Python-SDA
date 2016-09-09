#!/bin/env python

import sys


def unique(iterable):
    prev = None
    for val in iterable:
        if val != prev:
            yield val
        prev = val

if __name__ == '__main__':
    exec(sys.stdin.read())
