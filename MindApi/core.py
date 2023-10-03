import abc
import ast
import inspect
from typing import Any

from MindApi.builtin import Jump, MetaInstruction, Operation, Set
from MindApi.extension import PythonBuiltIn


class CodeConvert(ast.NodeVisitor):
    def __init__(self):
        self._instructions: list[MetaInstruction] = []

    # utility functions
    def push(self, instruction: MetaInstruction):
        self._instructions.append(instruction)

    def pop(self):
        return self._instructions.pop()

    def print_instructions(self):
        for i, inst in enumerate(self._instructions):
            print(f"{i}: {inst}")

    def mlog(self) -> str:
        self.print_instructions()
        return "\n".join([str(i) for i in self._instructions])

    def visit_Constant(self, node: ast.Constant) -> Any:
        if node.value is True:
            return 1
        elif node.value is False:
            return 0
        return node.value

    def visit_Assign(self, node: ast.Assign):
        if len(node.targets) != 1:
            raise NotImplementedError("Multiple assignments are not supported")
        if not isinstance(node.targets[0], ast.Name):
            raise NotImplementedError(
                f"Assign to {type(node.targets[0])} is not supported"
            )
        dest = self.visit_Name(node.targets[0])
        if isinstance(node.value, ast.Constant):  # Example: a = 1
            value = self.visit_Constant(node.value)
            self.push(Set(dest, value))
        elif isinstance(node.value, ast.BinOp):  # Example: a = b + c
            self.visit_BinOp(node.value)
            binInst: Operation = self.pop()  # type: ignore
            binInst.dest = dest
            self.push(binInst)
        elif isinstance(node.value, ast.Compare):  # Example: a = b > c
            self.visit_Compare(node.value)
            binInst: Operation = self.pop()  # type: ignore
            binInst.dest = dest
            self.push(binInst)
        elif isinstance(node.value, ast.BoolOp):  # Example: a = b and c
            self.visit_BoolOp(node.value)
            binInst: Operation = self.pop()  # type: ignore
            binInst.dest = dest
            self.push(binInst)
        elif isinstance(node.value, ast.UnaryOp):  # Example: a = - b
            raise NotImplementedError("Unary operation is not supported")
        elif isinstance(node.value, ast.Call):  # Example: a = abs(a)
            self.visit_Call(node.value)
            binInst: Operation = self.pop()  # type: ignore
            binInst.dest = dest
            self.push(binInst)
        elif isinstance(node.value, ast.Name):  # Example: a = b
            self.push(Set(dest, self.visit_Name(node.value)))
        else:
            raise NotImplementedError(
                f"Assign from {type(node.value)} is not supported"
            )

    def visit_Name(self, node: ast.Name) -> Any:
        if node.id == "pi":
            return 3.141592653589793
        if node.id == "e":
            return 2.718281828459045
        return node.id

    def visit_BoolOp(self, node: ast.BoolOp) -> Any:
        if len(node.values) != 2:
            raise NotImplementedError("Multiple boolean operations are not supported")
        left = self.visit(node.values[0])
        right = self.visit(node.values[1])
        dest = "__remove"
        op = node.op.__class__.__name__
        self.push(Operation(dest, left, op, right))

    def visit_UnaryOp(self, node: ast.UnaryOp) -> Any:
        if not isinstance(node.operand, ast.Name) and not isinstance(
            node.operand, ast.Constant
        ):
            raise NotImplementedError(
                f"Unary operation on {type(node.operand)} is not supported"
            )
        operand = self.visit(node.operand)
        dest = "__remove"
        op = node.op.__class__.__name__
        self.push(Operation(dest, "__remove", op, operand))

    def visit_BinOp(self, node: ast.BinOp):
        if isinstance(node.left, ast.BinOp) or isinstance(
            node.right, ast.BinOp
        ):  # Example: a + b + c
            raise NotImplementedError("Nested binary operations are not supported")
        left = self.visit(node.left)
        right = self.visit(node.right)
        dest = "__remove"
        op = node.op.__class__.__name__
        self.push(Operation(dest, left, op, right))

    def visit_While(self, node: ast.While):
        if isinstance(node.test, ast.Constant) or isinstance(node.test, ast.Name):
            self.visit_Compare(ast.Compare(node.test, [ast.Eq()], [ast.Constant(1)]))
            # transform the jump instruction
            binInst: Operation = self.pop()  # type: ignore
            self.push(Jump(binInst.left, binInst.op, binInst.right, -1))
            jumpIndex = len(self._instructions)
            for i in node.body:
                self.visit(i)
            self._instructions[jumpIndex - 1].to = len(self._instructions) + 1  # type: ignore
            # fill the break instruction
            for i in self._instructions[jumpIndex:]:  # type: ignore
                if isinstance(i, Jump) and i.to == -1:
                    i.to = len(self._instructions) + 1
            self.push(Jump("1", ast.Eq().__class__.__name__, "1", jumpIndex - 1))

    def visit_Break(self, node: ast.Break):
        self.push(Jump("1", ast.Eq().__class__.__name__, "1", -1))

    def visit_If(self, node: ast.If):
        if not isinstance(node.test, ast.Compare):
            raise NotImplementedError(f"If with {type(node.test)} is not supported")
        self.visit_Compare(node.test)
        # transform the jump instruction
        binInst: Operation = self.pop()  # type: ignore
        self.push(Jump(binInst.left, binInst.op, binInst.right, -1))
        jumpIndex = len(self._instructions)
        for i in node.body:
            self.visit(i)
        self._instructions[jumpIndex - 1].to = len(self._instructions)  # type: ignore
        for i in node.orelse:
            self.visit(i)

    def visit_Compare(self, node: ast.Compare):
        if not isinstance(node.left, ast.Name) and not isinstance(
            node.left, ast.Constant
        ):
            raise NotImplementedError(
                f"Comparison with {type(node.left)} is not supported"
            )
        left = self.visit(node.left)
        if len(node.ops) != 1:
            raise NotImplementedError("Multiple comparisons are not supported")
        op = node.ops[0].__class__.__name__
        if not isinstance(node.comparators[0], ast.Constant) and not isinstance(
            node.comparators[0], ast.Name
        ):
            raise NotImplementedError(
                f"Comparison with {type(node.comparators[0])} is not supported"
            )
        self.push(Operation("__remove", left, op, self.visit(node.comparators[0])))

    def visit_Pass(self, node: ast.Pass):
        pass

    def visit_Expr(self, node: ast.Expr):
        if isinstance(node.value, ast.Call):
            self.visit_Call(node.value)
        else:
            raise NotImplementedError(
                f"Expression with {type(node.value)} is not supported"
            )

    def visit_Call(self, node: ast.Call):
        if not isinstance(node.func, ast.Name):
            raise NotImplementedError(f"Call to {type(node.func)} is not supported")
        func_name = self.visit(node.func)
        try:
            func = getattr(PythonBuiltIn, func_name)
            func_inst = func(node.args)
            for i in func_inst:
                self.push(i)
        except AttributeError:
            raise ValueError(f"Invalid function name: {func_name}")

    def visit_AugAssign(self, node: ast.AugAssign):
        self.visit_Assign(
            ast.Assign([node.target], ast.BinOp(node.target, node.op, node.value))
        )


class CPUTemplate(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def init(self):
        pass

    @abc.abstractmethod
    def loop(self):
        pass


def compiler(cls: CPUTemplate):
    def pre_process(fn) -> str:
        # remove the 'def' from the source code
        code = inspect.getsource(fn).split("\n")[1:-1]
        # remove the indentation
        indent = len(code[0]) - len(code[0].lstrip())
        code = "\n".join([line[indent:] for line in code])  # type: ignore
        # remove the 'self' argument
        code = code.replace("self.", "")  # type: ignore
        return code  # type: ignore

    init, loop = pre_process(cls.init), pre_process(cls.loop)
    print(f"{init} \n---------\n{loop}")
    init_ast, loop_ast = ast.parse(init), ast.parse(loop)
    print(f"{ast.dump(init_ast)} \n---------\n{ ast.dump(loop_ast)}")
    init = CodeConvert()  # type: ignore
    loop = CodeConvert()  # type: ignore
    init.visit(init_ast)  # type: ignore
    loop.visit(loop_ast)  # type: ignore
    init_mlog = init.mlog()  # type: ignore # noqa
    loop_mlog = loop.mlog()  # type: ignore # noqa
    return cls
