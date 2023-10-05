from .test_compiler import TestCase


class TestWhile(TestCase):
    def init(self):
        while 1:
            self.a = 2
            break
        while self.a == 1:
            self.a = 2

        while 1:
            self.a = 2
            while 1:
                self.a = 2
                break
            self.a = 2

        while True:
            self.a = 2
            break
        while False:
            self.a = 2

    def loop(self):
        while 1:
            self.a = 2
            break
        a = 1
        print(a)
