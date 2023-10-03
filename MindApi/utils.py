binary_ops = {
    "Add": "add",
    "Sub": "sub",
    "Mult": "mul",
    "Div": "div",
    "Mod": "mod",
    "FloorDiv": "idiv",
    "Pow": "pow",
    "BitAnd": "and",
    "BitOr": "or",
    "BitXor": "xor",
    "LShift": "shl",
    "RShift": "shr",
}

condition_ops_inverse = {
    "Eq": "notEqual",
    "NotEq": "equal",
}

condition_ops = {
    "Eq": "equal",
    "NotEq": "notEqual",
    "Lt": "lessThan",
    "LtE": "lessThanEq",
    "Gt": "greaterThan",
    "GtE": "greaterThanEq",
}

binary_ops.update(condition_ops)
