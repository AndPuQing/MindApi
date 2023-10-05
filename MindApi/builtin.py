import abc
from typing import Union

from MindApi.types import MetaType, OperationType, UnitType
from MindApi.utils import binary_ops, condition_ops, condition_ops_inverse


class MetaInstruction(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __str__(self):
        pass


# ---------Input/Output---------#
class Read(MetaInstruction):
    def __init__(self, dest: str, src: str, index: str):
        self.dest = dest
        self.src = src
        self.index = index

    def __str__(self):
        return f"read {self.dest} {self.src} {self.index}"


class Write(MetaInstruction):
    def __init__(self, src: str, dest: str, index: str):
        self.dest = dest
        self.src = src
        self.index = index

    def __str__(self):
        return f"write {self.src} {self.dest} {self.index}"


class Draw(MetaInstruction):
    def __init__(self, cmd: str, *args):
        self.cmd = cmd
        self.args = args

    def __str__(self):
        args = list(self.args) + ["0"] * (6 - len(self.args))
        return f"draw {self.cmd} {' '.join(args)}"


class Print(MetaInstruction):
    def __init__(self, val: str, is_var: bool = False):
        self.val = val
        self.is_var = is_var

    def __str__(self):
        if self.is_var:
            return f"print {self.val}"
        else:
            return 'print "' + f"{self.val}" + '"'


# ---------Block Control---------#
class DrawFlush(MetaInstruction):
    def __init__(self, display: str):
        self.display = display

    def __str__(self):
        return f"drawflush {self.display}"


class PrintFlush(MetaInstruction):
    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return f"printflush {self.message}"


class GetLink(MetaInstruction):
    def __init__(self, dest: str, src: int):
        self.dest = dest
        self.src = src

    def __str__(self):
        return f"getlink {self.dest} {self.src}"


# ---------Operations---------#
class Set(MetaInstruction):
    def __init__(self, dest: str, src: Union[str, float, int]) -> None:
        self.dest = dest
        self.src = src

    def __str__(self) -> str:
        return f"set {self.dest} {self.src}"


class Operation(MetaInstruction):
    def __init__(
        self,
        dest: str,
        left: Union[str, float, int],
        op: Union[OperationType, str],
        right: Union[str, float, int],
    ) -> None:
        self.dest = dest
        self.left = left
        self.op = op
        self.right = right

    def __str__(self) -> str:
        if not isinstance(self.op, OperationType):
            try:
                op = binary_ops[self.op]
            except KeyError:
                raise ValueError(f"Invalid binary operator: {self.op}")
        else:
            op = self.op.value
        return f"op {self.dest} {self.left} {op} {self.right}"


class LookUp(MetaInstruction):
    def __init__(self, dest: str, type: MetaType, index: int):
        self.dest = dest
        self.type = type
        self.index = index

    def __str__(self):
        return f"lookup {self.type} {self.dest} {self.index}"


class PackColor(MetaInstruction):
    def __init__(self, dest: str, rgba_tuple: tuple = (1, 0, 0, 1)):
        self.dest = dest
        if len(rgba_tuple) != 4:
            raise ValueError("rgba_tuple must have 4 elements")
        for i in rgba_tuple:
            if i < 0 or i > 1:
                raise ValueError("rgba_tuple must be in range [0, 1]")
        self.r, self.g, self.b, self.a = rgba_tuple

    def __str__(self):
        return f"packcolor {self.dest} {self.r} {self.g} {self.b} {self.a}"


# ---------Flow Control---------#
class Jump(MetaInstruction):
    def __init__(
        self,
        left: Union[str, float, int],
        op: str,
        right: Union[str, float, int],
        to: Union[int, str],
        reverse=True,
    ):
        self.left = left
        self.op = op
        self.right = right
        self.to = to
        self.reverse = reverse

    def __str__(self) -> str:
        try:
            if self.reverse:
                op = condition_ops_inverse[self.op]
            else:
                op = condition_ops[self.op]
            return f"jump {self.to} {self.left} {op} {self.right}"
        except KeyError:
            raise ValueError(f"Invalid condition operator: {self.op}")


class Wait(MetaInstruction):
    def __init__(self, delay_seconds: float):
        self.time = delay_seconds

    def __str__(self):
        return f"wait {self.time}"


class Stop(MetaInstruction):
    """
    Stop the program
    """

    def __str__(self):
        return "stop"


class End(MetaInstruction):
    """
    Jump to the beginning of the program
    """

    def __str__(self):
        return "end"


# ---------Unit Control---------#
class UnitBind(MetaInstruction):
    def __init__(self, unitType: UnitType):
        self.unit_type = unitType

    def __str__(self):
        return f"ubind @{self.unit_type}"


class UnitControl(MetaInstruction):
    def __init__(self, actiontype: str, *args):
        self.actiontype = actiontype
        self.args = args

    def __str__(self):
        args = list(self.args) + ["0"] * (5 - len(self.args))
        return f"ucontrol {self.actiontype} {' '.join(args)}"


class UnitRadar(MetaInstruction):
    def __init__(
        self,
        dest: str,
        targetclass1: str,
        targetclass2: str,
        targetclass3: str,
        order: bool,
        sort: str,
    ):
        self.dest = dest
        self.targetclass1 = targetclass1
        self.targetclass2 = targetclass2
        self.targetclass3 = targetclass3
        self.order = order
        self.sort = sort

    def __str__(self):
        return f"uradar {self.targetclass1} {self.targetclass2} {self.targetclass3} {self.order} {self.sort} {self.dest}"


class UnitLocate(MetaInstruction):
    def __init__(
        self,
        outX: str,
        outY: str,
        Found: str,
        building: str,
        find: str,
        group: str,
        enemy: str,
    ):
        self.outX = outX
        self.outY = outY
        self.Found = Found
        self.building = building
        self.find = find
        self.group = group
        self.enemy = enemy

    def __str__(self):
        return f"ulocate {self.find} {self.group} {self.enemy} @copper {self.outX} {self.outY} {self.Found} {self.building}"
