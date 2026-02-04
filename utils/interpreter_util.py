import ast
from typing import List, Any

from core.memory import global_variables


def normalize_name(name: str) -> str:
    return name.strip().lower()


def get_function_parameters(call: str) -> List[Any]:
    node = ast.parse(call, mode="eval")
    params = []

    for arg in node.body.args:
        if isinstance(arg, ast.Constant):
            params.append(arg.value)
            continue

        if isinstance(arg, ast.Name):
            name = normalize_name(arg.id)
            if name not in global_variables:
                raise NameError(f"Variable '{name}' not defined")
            params.append(global_variables[name].value)
            continue

        raise ValueError("Unsupported parameter type")

    return params
