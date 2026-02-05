import ast

from core.operators import interpret_node, preprocess


def get_function_parameters(call: str):
    node = ast.parse(call, mode="eval")
    return [interpret_node(arg) for arg in node.body.args]
