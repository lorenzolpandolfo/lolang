import ast
from typing import List, Any

from core.memory import global_variables
from core.variable import Variable
from utils.log import log
from enums.type import Type


def get_function_parameters(call: str) -> List[Any]:
    # se esta definindo um campo numa variavel
    if " = " in call and len(call.split(" = ", 1)) == 2 and call.startswith("int"): # todo: ajustar
        call = call.split("=")[1].strip()

    node = ast.parse(call, mode="eval")
    params = []

    for arg in node.body.args:
        if isinstance(arg, ast.Constant):
            params.append(arg.value)

        elif isinstance(arg, ast.Name):
            var_name = arg.id.strip().lower()

            if global_variables.get(var_name) is not None:
                params.append(global_variables.get(var_name).value)


            if not global_variables.get(var_name):
                pass

        else:
            raise ValueError("Unsupported parameter type")

    return params


def sanitize_parameter(param: str) -> str:
    return param.strip().replace('"', "")
