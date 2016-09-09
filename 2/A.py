import sys


class Rational:

    def __init__(self, n=0, m=1):
        x = abs(n)
        y = abs(m)
        while y > 0 and x > 0:
            if x > y:
                x = x % y
            else:
                y = y % x
        n //= (x + y)
        m //= (x + y)
        if n * m > 0:
            n = abs(n)
        else:
            n = -abs(n)
        m = abs(m)
        self.m = m
        self.n = n

    def __add__(self, other):
        return Rational(self.n * other.m + self.m * other.n, self.m * other.m)

    def __sub__(self, other):
        return Rational(self.n * other.m - self.m * other.n, self.m * other.m)

    def __mul__(self, other):
        return Rational(self.n * other.n, self.m * other.m)

    def __div__(self, other):
        return Rational(self.n * other.m, self.m * other.n)

    def __eq__(self, other):
        return self.n == other.n and self.m == other.m

    def __ne__(self, other):
        return self.n != other.n or self.m != other.m

    def __neg__(self):
        return Rational(-self.n, self.m)

    def __str__(self):
        return str(self.n) + '/' + str(self.m)

exec(sys.stdin.read())
