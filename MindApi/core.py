import abc
import ast
import inspect
from typing import Any, Callable, List

from MindApi.builtin import Jump, MetaInstruction, Operation, Set
from MindApi.extension import PythonBuiltIn


class CodeConvert(ast.NodeVisitor):
    def __init__(self, cls):
        self.cls = cls
        self._instructions: list[MetaInstruction] = []
        self._fn_list: dict[str, list[MetaInstruction]] = {}

    # utility functions
    def push(self, instruction: MetaInstruction):
        self._instructions.append(instruction)

    def pop(self):
        return self._instructions.pop()

    def print_instructions(self):
        for i, inst in enumerate(self._instructions):
            print(f"{i}: {inst}")

    def mlog(self) -> str:
        return "\n".join([str(i) for i in self._instructions])

    def fn_code_process(self, fn: Callable) -> ast.AST:
        fn_code = pre_process(fn)
        # var name isolation
        fn_ast = ast.parse(fn_code)

        class FnVarNameIsolation(ast.NodeTransformer):
            def visit_Call(self, node: ast.Call) -> ast.Call:
                for arg in node.args:
                    self.visit(arg)
                return node

            def visit_Name(self, node: ast.Name) -> ast.Name:
                if node.id.startswith("__"):
                    return node
                node.id = f"__{fn.__name__}_{node.id}"
                return node

        return FnVarNameIsolation().visit(fn_ast)

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
        elif isinstance(node.test, ast.Compare):
            self.visit_Compare(node.test)
            binInst: Operation = self.pop()  # type: ignore
            self.push(Jump(binInst.left, binInst.op, binInst.right, -1))
            jumpIndex = len(self._instructions)
            for i in node.body:
                self.visit(i)
            self._instructions[jumpIndex - 1].to = len(self._instructions) + 1  # type: ignore
        else:
            raise NotImplementedError(f"While with {type(node.test)} is not supported")
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
        if func_name.startswith("__"):
            try:
                func = getattr(self.cls, func_name[2:])
                func_ast = self.fn_code_process(func)
                func_convert = CodeConvert(self.cls)
                func_convert.visit(func_ast)
                if not isinstance(func_convert._instructions[-1], Jump):
                    func_convert.push(
                        Jump("1", ast.Eq().__class__.__name__, "1", "__jumpback")
                    )
                self._fn_list[func_name] = func_convert._instructions
                for arg_value, arg_name in zip(
                    node.args,
                    func.__code__.co_varnames[1 : func.__code__.co_argcount],
                ):
                    if isinstance(arg_value, ast.Constant):
                        self.push(Set(f"__{func.__name__}_{arg_name}", arg_value.value))
                    elif isinstance(arg_value, ast.Name):
                        self.push(Set(f"__{func.__name__}_{arg_name}", arg_value.id))
                    else:
                        raise NotImplementedError(
                            f"Call with {type(arg_value)} is not supported"
                        )

                self.push(Set("__jumpback", len(self._instructions) + 2))
                self.push(
                    Jump("1", ast.Eq().__class__.__name__, "1", f"__remove_{func_name}")
                )
                self.push(Set("__remove", "__return"))
            except AttributeError:
                raise ValueError(f"Invalid function name: {func_name}")
        else:
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

    def visit_Return(self, node: ast.Return):
        if node.value is None:
            pass
        else:
            if isinstance(node.value, ast.Constant):
                self.push(Set("__return", node.value.value))
            elif isinstance(node.value, ast.Name):
                self.push(Set("__return", node.value.id))
            elif isinstance(node.value, ast.BinOp):
                self.visit_BinOp(node.value)
                binInst: Operation = self.pop()  # type: ignore
                binInst.dest = "__return"
                self.push(binInst)
        self.push(Jump("1", ast.Eq().__class__.__name__, "1", "__jumpback"))

    @property
    def fn_list(self):
        return self._fn_list

    @property
    def instructions(self):
        return self._instructions


class CPUTemplate(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def loop(self):
        pass


def pre_process(fn) -> str:
    # remove the 'def' from the source code
    code = inspect.getsource(fn).split("\n")[1:-1]
    # remove the indentation
    indent = len(code[0]) - len(code[0].lstrip())
    code = "\n".join([line[indent:] for line in code])  # type: ignore
    # remove the 'self' argument
    code = code.replace("self.", "__")  # type: ignore
    return code  # type: ignore


def convert(fn: Callable, cls: CPUTemplate) -> CodeConvert:
    code = ast.parse(pre_process(fn))
    convert = CodeConvert(cls)
    convert.visit(code)
    convert.print_instructions()
    return convert


def compiler(cls: CPUTemplate):
    function_map = {}
    instructions = List[MetaInstruction]
    if hasattr(cls, "init"):
        init = getattr(cls, "init")
        code = convert(init, cls)
        function_map.update(code.fn_list)
        instructions += code.instructions
    if hasattr(cls, "loop"):
        loop = getattr(cls, "loop")
        code = convert(loop, cls)
        function_map.update(code.fn_list)
        # every jump instruction should be shifted
        for inst in code.instructions:
            if isinstance(inst, Jump) and isinstance(inst.to, int):
                inst.to += len(instructions)  # type: ignore
        code.push(
            Jump("1", ast.Eq().__class__.__name__, "1", len(instructions))  # type: ignore
        )  # loop jump
        instructions += code.instructions
    # process the function map
    index_map = {}
    for fn_name, fn_inst in function_map.items():
        index_map[fn_name] = len(instructions)  # type: ignore
        instructions += fn_inst
    # process the jump instruction
    for inst in instructions:  # type: ignore
        if isinstance(inst, Jump) and isinstance(inst.to, str):
            if inst.to.startswith("__remove_"):
                inst.to = index_map[inst.to[9:]]
    return instructions
