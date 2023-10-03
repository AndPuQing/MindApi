from MindApi import CPUTemplate, compiler


def test_if():
    @compiler
    class TEST_CPU(CPUTemplate):
        def init(self):
            a = 1
            if a == 1:
                a = 2
                a = 2
                a = 2
                a = 2
            elif a == 2:
                a = 3
                a = 2
                a = 2
            else:
                a = 4
            print(a)

        def loop(self):
            if self.a == 1:
                self.a = 2
                self.a = 2
            elif self.a == 2:
                self.a = 3
            else:
                self.a = 4
            print(self.a)
