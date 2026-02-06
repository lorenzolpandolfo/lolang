import ast
import operator
from typing import Any, Dict

from core.constants.core_functions import CORE_FUNCTIONS
from core.memory import GLOBAL_VARIABLES, USER_FUNCTIONS

_EXPR_CACHE: Dict[str, Any] = {}
_COMPILED_CACHE: Dict[str, Any] = {}

_BINOP_HANDLERS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.FloorDiv: operator.floordiv,
}

_COMPARE_HANDLERS = {
    ast.Eq: operator.eq,
    ast.NotEq: operator.ne,
    ast.Lt: operator.lt,
    ast.LtE: operator.le,
    ast.Gt: operator.gt,
    ast.GtE: operator.ge,
}

_BOOLOP_HANDLERS = {
    ast.And: all,
    ast.Or: any,
}

_UNARYOP_HANDLERS = {
    ast.Not: operator.not_,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

_SPECIAL_FUNCTIONS = {
    "root": lambda value, degree: value ** (1 / degree),
    "equals_ignore_type": lambda a, b: str(a) == str(b),
    "not_equals_ignore_type": lambda a, b: str(a) != str(b),
}


def interpret_expression(expr: str):
    if expr in _EXPR_CACHE:
        node = _EXPR_CACHE[expr]
    else:
        preprocessed = preprocess(expr)
        node = ast.parse(preprocessed, mode="eval").body
        _EXPR_CACHE[expr] = node

    return interpret_node(node)


def preprocess(expr: str) -> str:
    if expr in _COMPILED_CACHE:
        return _COMPILED_CACHE[expr]

    result = expr
    if "&&" in expr:
        result = result.replace("&&", " and ")
    if "||" in expr:
        result = result.replace("||", " or ")

    if "===" in result:
        a, b = result.split("===", 1)
        result = f"equals_ignore_type({a.strip()}, {b.strip()})"
    elif "!==" in result:
        a, b = result.split("!==", 1)
        result = f"not_equals_ignore_type({a.strip()}, {b.strip()})"
    elif "$" in result:
        a, b = result.split("$", 1)
        result = f"root({a.strip()}, {b.strip()})"

    _COMPILED_CACHE[expr] = result
    return result


def interpret_node(node):
    """Versão otimizada com dispatch table e cache"""
    node_type = type(node)

    if node_type is ast.Constant:
        return node.value

    if node_type is ast.Name:
        name = node.id
        if name.lower() == "true":
            return True
        if name.lower() == "false":
            return False

        var = GLOBAL_VARIABLES.get(name)
        if var is None:
            raise ValueError(f"Variable '{name}' not defined")
        return var.value

    if node_type is ast.BinOp:
        left = interpret_node(node.left)
        right = interpret_node(node.right)

        handler = _BINOP_HANDLERS.get(type(node.op))
        if handler:
            return handler(left, right)
        raise ValueError(f"Unsupported operator: {type(node.op)}")

    if node_type is ast.Compare:
        left = interpret_node(node.left)
        right = interpret_node(node.comparators[0])
        op = node.ops[0]

        handler = _COMPARE_HANDLERS.get(type(op))
        if handler:
            return handler(left, right)
        raise ValueError(f"Unsupported comparison: {type(op)}")

    if node_type is ast.BoolOp:
        op_type = type(node.op)

        if op_type is ast.And:
            for value_node in node.values:
                if not interpret_node(value_node):
                    return False
            return True

        if op_type is ast.Or:
            for value_node in node.values:
                if interpret_node(value_node):
                    return True
            return False

        raise ValueError(f"Unsupported boolean operator: {op_type}")

    if node_type is ast.Call:
        func_name = node.func.id

        args = [interpret_node(arg) for arg in node.args]

        special_func = _SPECIAL_FUNCTIONS.get(func_name)
        if special_func:
            return special_func(*args)

        core_func = CORE_FUNCTIONS.get(func_name)
        if core_func:
            return core_func(args)

        user_func = USER_FUNCTIONS.get(func_name)
        if user_func:
            from lolang import call_user_function
            return call_user_function(user_func, args, False, "")

        raise ValueError(f"Unknown function '{func_name}'")

    if node_type is ast.List:
        return [interpret_node(el) for el in node.elts]

    if node_type is ast.Subscript:
        value = interpret_node(node.value)

        if isinstance(node.slice, ast.Index):
            index = interpret_node(node.slice.value)
        elif isinstance(node.slice, ast.Constant):
            index = node.slice.value
        else:
            index = interpret_node(node.slice)

        return value[index]

    if node_type is ast.UnaryOp:
        value = interpret_node(node.operand)
        op_type = type(node.op)

        handler = _UNARYOP_HANDLERS.get(op_type)
        if handler:
            return handler(value)

        raise ValueError(f"Unsupported unary operator: {op_type}")

    if node_type is ast.Tuple:
        return tuple(interpret_node(el) for el in node.elts)

    if node_type is ast.Dict:
        keys = [interpret_node(k) for k in node.keys]
        values = [interpret_node(v) for v in node.values]
        return dict(zip(keys, values))

    if node_type is ast.Set:
        return {interpret_node(el) for el in node.elts}

    raise ValueError(f"Unsupported expression type: {node_type}")
