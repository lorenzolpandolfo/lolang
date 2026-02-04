import os
import sys
from typing import List, Callable

from constants.core_functions import CORE_FUNCTIONS
from core.memory import global_variables
from core.operators import eval_expression
from core.variable import Variable
from utils.interpreter_util import get_function_parameters
from utils.log import log
from enums.type import Type


def validate_file(filename: str) -> bool:
    return os.path.isfile(filename) and os.access(filename, os.R_OK) and filename.endswith(".lo")


def validate_args() -> None:
    args: List[str] = sys.argv[1:]

    if len(args) != 1:
        raise FileNotFoundError("Invalid number of arguments.")

    filename: str = args[0]

    if not validate_file(filename):
        raise FileNotFoundError(filename, "Invalid .lo file: " + filename)


def load_file_content() -> None:
    args: List[str] = sys.argv[1:]
    filename: str = args[0]

    with open(filename, "r") as f:
        content = f.readlines()

        for line in content:
            interpret_line_content(line)


def interpret_line_content(data: str) -> None:
    if data == "\n" or data == "":
        return

    if f"{data[0]}{data[1]}" == "//" or data[0] == "#":
        return

    tokens: List[str] = tokenize(data)
    tokens = [t.strip() for t in tokens]

    for t in tokens:
        if t == "":
            continue

        handle_core_functions(t)


def tokenize(data: str) -> List[str]:
    return data.split(";")


def handle_core_functions(data: str) -> None:
    if handle_function_process(data):
        return

    if handle_variable_process(data):
        return


def handle_function_process(data: str) -> bool:
    if not "(" in data or not ")" in data:
        return False

    if "=" in data:
        function_name = data.split("=")[1].split("(", 1)[0].strip().lower()
    else:
        function_name = data.split("(", 1)[0].strip().lower()

    # o problema eh que o valor ta vindo None
    params: List[str] = get_function_parameters(data)
    function_to_call: Callable = CORE_FUNCTIONS.get(function_name)

    if not function_to_call:
        return False

    r = function_to_call(params)

    if r:
        var_type, var_name = data.split("=")[0].split(" ", 1)

        var_type = var_type.strip().lower()
        var_name = var_name.strip().lower()

        register_variable(var_name, str(var_type), str(r))
        global_variables.get(var_name).value = r
    return True


def handle_variable_process(data: str) -> bool:
    parts = data.split(" = ", 1)
    if len(parts) != 2:
        return False

    left, right = parts
    type_name, var_name = left.strip().split(" ", 1)
    value = right.strip()

    if not Type.is_valid_type(type_name):
        return False

    register_variable(var_name, type_name, value)
    return True


def register_variable(var_name: str, type_name: str, value = None) -> None:
    variable = Variable(name=var_name, v_type=Type[type_name.upper()])

    evaluated_value = eval_expression(value)
    variable.set_value(evaluated_value)
    global_variables[var_name] = variable



if __name__ == "__main__":
    validate_args()
    load_file_content()
