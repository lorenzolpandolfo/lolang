import ast
import re

from core.memory import global_variables
from constants.core_functions import CORE_FUNCTIONS
from utils.log import log


def eval_expression(expr: str):
    node = ast.parse(preprocess(expr), mode="eval")
    return interpret_node(node.body)

def preprocess(expr: str) -> str:
    expr = expr.replace("&&", " and ")
    expr = expr.replace("||", " or ")
    # expr = re.sub(r'!(?!=)', ' not ', expr)

    if "===" in expr:
        a, b = expr.split("===", 1)
        return f"equals_ignore_type({a.strip()}, {b.strip()})"

    if "!==" in expr:
        a, b = expr.split("!==", 1)
        return f"not_equals_ignore_type({a.strip()}, {b.strip()})"

    if "$" in expr:
        a, b = expr.split("$", 1)
        return f"root({a.strip()}, {b.strip()})"
    return expr


def interpret_node(node):
    if isinstance(node, ast.Constant):
        return node.value

    if isinstance(node, ast.Name):
        if node.id.lower() == "true":
            return True
        elif node.id.lower() == "false":
            return False

        var = global_variables.get(node.id)
        if not var:
            raise ValueError(f"Variable '{node.id}' not defined")
        return var.value

    if isinstance(node, ast.BinOp):
        left = interpret_node(node.left)
        right = interpret_node(node.right)

        if isinstance(node.op, ast.Add):
            return left + right
        if isinstance(node.op, ast.Sub):
            return left - right
        if isinstance(node.op, ast.Mult):
            return left * right
        if isinstance(node.op, ast.Div):
            return left / right
        if isinstance(node.op, ast.Pow):
            return left ** right
        if isinstance(node.op, ast.Mod):
            return left % right
        raise ValueError("Unsupported operator")

    if isinstance(node, ast.Compare):
        left = interpret_node(node.left)
        right = interpret_node(node.comparators[0])
        op = node.ops[0]

        if isinstance(op, ast.Eq):
            return left == right
        if isinstance(op, ast.NotEq):
            return left != right
        if isinstance(op, ast.Lt):
            return left < right
        if isinstance(op, ast.LtE):
            return left <= right
        if isinstance(op, ast.Gt):
            return left > right
        if isinstance(op, ast.GtE):
            return left >= right

        raise ValueError("Unsupported comparison")

    if isinstance(node, ast.BoolOp):
        if isinstance(node.op, ast.And):
            return all(interpret_node(v) for v in node.values)

        if isinstance(node.op, ast.Or):
            return any(interpret_node(v) for v in node.values)

        raise ValueError("Unsupported boolean operator")

    if isinstance(node, ast.Call):
        func_name = node.func.id
        args = [interpret_node(arg) for arg in node.args]

        if func_name == "root":
            value, degree = args
            return value ** (1 / degree)

        if func_name == "equals_ignore_type":
            a, b = args
            return str(a) == str(b)

        if func_name == "not_equals_ignore_type":
            a, b = args
            return str(a) != str(b)

        if func_name in CORE_FUNCTIONS:
            return CORE_FUNCTIONS[func_name](args)

        raise ValueError(f"Unknown function '{func_name}'")

    if isinstance(node, ast.List):
        return [interpret_node(el) for el in node.elts]

    if isinstance(node, ast.Subscript):
        value = interpret_node(node.value)
        index = interpret_node(node.slice)
        return value[index]

    if isinstance(node, ast.UnaryOp):
        value = interpret_node(node.operand)

        if isinstance(node.op, ast.Not):
            return not value

        if isinstance(node.op, ast.USub):
            return not -value

        if isinstance(node.op, ast.UAdd):
            return +value

        raise ValueError("Unsupported unary operator")

    raise ValueError("Unsupported expression")
