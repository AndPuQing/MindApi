from .test_compiler import Compiler, TestCase


@Compiler()
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


@Compiler()
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
        self.fn(1, self.a)

    def loop(self):
        print("mindustry")


@Compiler()
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


@Compiler()
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
