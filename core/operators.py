import ast

from core.memory import global_variables
from constants.core_functions import CORE_FUNCTIONS
from utils.log import log


def eval_expression(expr: str):
    node = ast.parse(preprocess(expr), mode="eval")
    return _eval_node(node.body)

def preprocess(expr: str) -> str:
    expr = expr.replace("&&", " and ")
    expr = expr.replace("||", " or ")
    # expr = expr.replace(" ! ", " not ")

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


def _eval_node(node):
    if isinstance(node, ast.Constant):
        return node.value

    if isinstance(node, ast.Name):
        if node.id.lower() == "true" or node.id.lower() == "false":
            return bool(node.id)

        var = global_variables.get(node.id)
        if not var:
            raise ValueError(f"Variable '{node.id}' not defined")
        return var.value

    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)


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
        left = _eval_node(node.left)
        right = _eval_node(node.comparators[0])
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
            return all(_eval_node(v) for v in node.values)

        if isinstance(node.op, ast.Or):
            return any(_eval_node(v) for v in node.values)

        raise ValueError("Unsupported boolean operator")

    if isinstance(node, ast.Call):
        func_name = node.func.id

        args = [_eval_node(arg) for arg in node.args]

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

    raise ValueError("Unsupported expression")
