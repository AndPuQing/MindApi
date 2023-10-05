from .test_compiler import TestCase


class TestCall(TestCase):
    def fn(self):
        b = 2
        b += b
        b -= self.a
        print(b)
        print(self.a)

    def init(self):
        self.a = 1
        self.fn()

    def loop(self):
        print("mindustry")


class TestWithArgs(TestCase):
    def fn(self, a, b):
        b += b
        b -= self.a
        b -= a
        print(b)
        print(self.a)

    def init(self):
        self.a = 1
        self.fn(1, 1)

    def loop(self):
        print("mindustry")


class TestWithReturn(TestCase):
    def fn(self, a, b):
        return a
        return a * b
        return a + b
        return a + b

    def init(self):
        self.a = 1
        self.fn(1, 1)

    def loop(self):
        print("mindustry")


class TestCallAssiginReturn(TestCase):
    def fn(self, a, b):
        return a
        return a * b
        return a + b
        return a + b

    def init(self):
        self.a = 1
        a = self.fn(1, 1)
        print(a)

    def loop(self):
        print("mindustry")
