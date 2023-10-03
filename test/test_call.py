from MindApi import CPUTemplate, compiler


def test_call():
    @compiler
    class TEST_CPU(CPUTemplate):
        def init(self):
            a = 1
            print(a)
            # print(f"what is it {a} asdf") # TODO: support f-string

        def loop(self):
            b = 1
            print(b)
            print("alskdjfasdf")
