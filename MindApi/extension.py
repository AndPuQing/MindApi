import math
from ast import Constant, Name, expr
from typing import List

from MindApi.builtin import Operation, Print, Set
from MindApi.types import OperationType


class PythonBuiltIn(object):
    @staticmethod
    def print(args: List[expr]):
        if len(args) != 1:
            raise NotImplementedError(f"print with {len(args)} arguments")
        if isinstance(args[0], Name):
            return [Print(args[0].id, True)]
        elif isinstance(args[0], Constant):
            return [Print(args[0].value, False)]
        else:
            raise NotImplementedError(f"print with {type(args[0])} as argument")

    @staticmethod
    def abs(args: List[expr]):
        if len(args) != 1:
            raise NotImplementedError(f"abs with {len(args)} arguments")
        if isinstance(args[0], Name):
            return [Operation("__remove", args[0].id, OperationType.Abs, "__unused")]
        elif isinstance(args[0], Constant):
            return [Operation("__remove", args[0].value, OperationType.Abs, "__unused")]
        else:
            raise NotImplementedError(f"abs with {type(args)} as argument")

    @staticmethod
    def divmod(args: List[expr]):
        raise NotImplementedError("divmod is not supported")

    @staticmethod
    def pow(args: List[Constant | Name]):
        if len(args) != 2:
            raise NotImplementedError(f"pow with {len(args)} arguments")
        if isinstance(args[0], Constant) and isinstance(args[1], Constant):
            return [Set("__remove", args[0].value ** args[1].value)]
        else:
            base = args[0].id if isinstance(args[0], Name) else args[0].value
            exp = args[1].id if isinstance(args[1], Name) else args[1].value
            return [Operation("__remove", base, OperationType.Pow, exp)]

    @staticmethod
    def max(args: List[Constant | Name]):
        if len(args) != 2:
            raise NotImplementedError(f"max with {len(args)} arguments")
        if isinstance(args[0], Constant) and isinstance(args[1], Constant):
            return [Set("__remove", max(args[0].value, args[1].value))]
        else:
            left = args[0].id if isinstance(args[0], Name) else args[0].value
            right = args[1].id if isinstance(args[1], Name) else args[1].value
            return [Operation("__remove", left, OperationType.Max, right)]

    @staticmethod
    def min(args: List[Constant | Name]):
        if len(args) != 2:
            raise NotImplementedError(f"min with {len(args)} arguments")
        if isinstance(args[0], Constant) and isinstance(args[1], Constant):
            return [Set("__remove", min(args[0].value, args[1].value))]
        else:
            left = args[0].id if isinstance(args[0], Name) else args[0].value
            right = args[1].id if isinstance(args[1], Name) else args[1].value
            return [Operation("__remove", left, OperationType.Min, right)]

    @staticmethod
    def log(args: List[Constant | Name]):
        if len(args) != 1:
            raise NotImplementedError(f"log with {len(args)} arguments")
        if isinstance(args[0], Constant):
            return [Set("__remove", math.log(args[0].value))]
        else:
            return [Operation("__remove", args[0].id, OperationType.Log, "__unused")]

    @staticmethod
    def log10(args: List[Constant | Name]):
        if len(args) != 1:
            raise NotImplementedError(f"log10 with {len(args)} arguments")
        if isinstance(args[0], Constant):
            return [Set("__remove", math.log10(args[0].value))]
        else:
            return [Operation("__remove", args[0].id, OperationType.Log10, "__unused")]

    @staticmethod
    def sqrt(args: List[Constant | Name]):
        if len(args) != 1:
            raise NotImplementedError(f"sqrt with {len(args)} arguments")
        if isinstance(args[0], Constant):
            return [Set("__remove", math.sqrt(args[0].value))]
        else:
            return [Operation("__remove", args[0].id, OperationType.Sqrt, "__unused")]

    @staticmethod
    def exp(args: List[Constant | Name]):
        if len(args) != 1:
            raise NotImplementedError(f"exp with {len(args)} arguments")
        if isinstance(args[0], Constant):
            return [Set("__remove", math.exp(args[0].value))]
        else:
            return [Operation("__remove", math.e, OperationType.Pow, args[0].id)]

    @staticmethod
    def round(args: List[expr]):
        raise NotImplementedError("round is not supported")

    @staticmethod
    def cos(args: List[Constant | Name]):
        if len(args) != 1:
            raise NotImplementedError(f"cos with {len(args)} arguments")
        if isinstance(args[0], Constant):
            return [Set("__remove", math.cos(args[0].value))]
        else:
            return [Operation("__remove", args[0].id, OperationType.Cos, "__unused")]

    @staticmethod
    def sin(args: List[Constant | Name]):
        if len(args) != 1:
            raise NotImplementedError(f"sin with {len(args)} arguments")
        if isinstance(args[0], Constant):
            return [Set("__remove", math.sin(args[0].value))]
        else:
            return [Operation("__remove", args[0].id, OperationType.Sin, "__unused")]

    @staticmethod
    def tan(args: List[Constant | Name]):
        if len(args) != 1:
            raise NotImplementedError(f"tan with {len(args)} arguments")
        if isinstance(args[0], Constant):
            return [Set("__remove", math.tan(args[0].value))]
        else:
            return [Operation("__remove", args[0].id, OperationType.Tan, "__unused")]

    @staticmethod
    def acos(args: List[Constant | Name]):
        if len(args) != 1:
            raise NotImplementedError(f"acos with {len(args)} arguments")
        if isinstance(args[0], Constant):
            return [Set("__remove", math.acos(args[0].value))]
        else:
            return [Operation("__remove", args[0].id, OperationType.Acos, "__unused")]

    @staticmethod
    def asin(args: List[Constant | Name]):
        if len(args) != 1:
            raise NotImplementedError(f"asin with {len(args)} arguments")
        if isinstance(args[0], Constant):
            return [Set("__remove", math.asin(args[0].value))]
        else:
            return [Operation("__remove", args[0].id, OperationType.Asin, "__unused")]

    @staticmethod
    def atan(args: List[Constant | Name]):
        if len(args) != 1:
            raise NotImplementedError(f"atan with {len(args)} arguments")
        if isinstance(args[0], Constant):
            return [Set("__remove", math.atan(args[0].value))]
        else:
            return [Operation("__remove", args[0].id, OperationType.Atan, "__unused")]

    @staticmethod
    def degrees(args: List[Constant | Name]):
        if len(args) != 1:
            raise NotImplementedError(f"degrees with {len(args)} arguments")
        if isinstance(args[0], Constant):
            return [Set("__remove", math.degrees(args[0].value))]
        else:
            return [Operation("__remove", 180 / math.pi, OperationType.Mul, args[0].id)]

    @staticmethod
    def radians(args: List[Constant | Name]):
        if len(args) != 1:
            raise NotImplementedError(f"radians with {len(args)} arguments")
        if isinstance(args[0], Constant):
            return [Set("__remove", math.radians(args[0].value))]
        else:
            return [Operation("__remove", math.pi / 180, OperationType.Mul, args[0].id)]

    @staticmethod
    def hypot(args: List[Constant | Name]):
        if len(args) != 2:
            raise NotImplementedError(f"hypot with {len(args)} arguments")
        if isinstance(args[0], Constant) and isinstance(args[1], Constant):
            return [Set("__remove", math.hypot(args[0].value, args[1].value))]
        else:
            x = args[0].id if isinstance(args[0], Name) else args[0].value
            y = args[1].id if isinstance(args[1], Name) else args[1].value
            return [Operation("__remove", x, OperationType.Angle, y)]
