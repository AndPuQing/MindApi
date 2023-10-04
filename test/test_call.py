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
            print("mindustry")


def test_call_usedefince():
    @compiler
    class TEST_CPU(CPUTemplate):
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


def test_call_args():
    @compiler
    class TEST_CPU(CPUTemplate):
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


def test_call_return():
    @compiler
    class TEST_CPU(CPUTemplate):
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


def test_call_assigin_return():
    @compiler
    class TEST_CPU(CPUTemplate):
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
