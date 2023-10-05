from math import (
    acos,
    asin,
    atan,
    cos,
    degrees,
    e,
    exp,
    hypot,
    log,
    log10,
    pi,
    radians,
    sin,
    sqrt,
    tan,
)

from .test_compiler import TestCase


class TestMath(TestCase):
    def init(self):
        self.a = 1 + 1
        self.a = 2
        self.a = 2
        self.a = 2
        self.a = 2
        b = 2
        b = 1 < 2
        b = 1 > 2
        b = 1 <= 2
        b = 1 >= 2
        b = 1 == 2
        b = 1 != 2
        b = 1 + 2
        b = 2 - 2
        b = 2 * 2
        b = 2 / 2
        b = 2 // 2
        b = 2 % 2
        b = 2**2
        b = 2 & 2
        b = 2 | 2
        b = 2 ^ 2
        b = 2 << 2
        b = 2 >> 2
        # b = 2 or 2  # TODO: support or operation
        # b = 2 and 2  # TODO: support and operation
        # b = not 2 # TODO: support unary operation
        # b = -2  # TODO: support unary operation
        # b = -b  # TODO: support unary operation
        print(b)

    def loop(self):
        self.a += 1
        self.a -= 1
        self.a /= 1
        self.a *= 1
        self.a %= 1


class TestBuiltinMathFn(TestCase):
    def init(self):
        b = 1
        b = abs(1)
        # b = divmod(1, 2)
        b = pow(1, 2)
        b = pow(b, 2)
        # b = round(1) # TODO: support round
        # b = round(1, 2)
        # b = round(1, -2)
        b = max(1, 2)
        b = min(1, 2)
        # b = sum([1, 2])
        # b = sum([1, 2], 3)
        # # b = len([1, 2]) # TODO: support len
        # b = len("asdf")
        print(b)

    def loop(self):
        pass


class TestMathFn(TestCase):
    def init(self):
        b = 1
        b = log(b)
        b = log10(123)
        b = sqrt(1)
        b = exp(123)
        b = cos(b)
        b = sin(b)
        b = tan(b)
        b = acos(b)
        b = asin(b)
        b = atan(b)
        b = degrees(b)
        b = radians(b)
        b = hypot(b, 1)
        b = pi
        b = e
        print(b)

    def loop(self):
        pass
