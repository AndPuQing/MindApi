import unittest

from MindApi import compiler


class Compiler:
    def __call__(self, cls):
        self.cpu = cls
        self.cpu.test_removeFlag = self.test_removeFlag
        return cls

    def test_removeFlag(self):
        instructions = compiler(self.cpu)
        for inst in instructions:
            assert "__remove" not in str(inst)


@Compiler()
class TestCase(unittest.TestCase):
    def init(self):
        pass

    def loop(self):
        pass
