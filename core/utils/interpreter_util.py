import ast

from core.interpreter import interpret_node


def get_function_parameters(call: str):
    node = ast.parse(call, mode="eval")
    return [interpret_node(arg) for arg in node.body.args]
