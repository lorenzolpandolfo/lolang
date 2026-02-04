import ast
from typing import List, Any

from core.memory import global_variables
from core.operators import _eval_node


def normalize_name(name: str) -> str:
    return name.strip().lower()

def get_function_parameters(call: str):
    node = ast.parse(call, mode="eval")
    params = []

    for arg in node.body.args:
        params.append(_eval_node(arg))

    return params

