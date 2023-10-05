from MindApi import CPUTemplate, compiler


def test_while():
    @compiler
    class TEST_CPU(CPUTemplate):
        def __init__(self):
            while 1:
                self.a = 2
                break
            while self.a == 1:
                self.a = 2
            #
            # while 1:
            #     self.a = 2
            #     while 1:
            #         self.a = 2
            #         break
            #     self.a = 2
            #
            # while True:
            #     self.a = 2
            #     break
            # while False:
            #     self.a = 2

        def loop(self):
            while 1:
                self.a = 2
                break
            a = 1
