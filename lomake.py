import os
import sys
from typing import List

from constants.core_functions import CORE_FUNCTIONS
from core.memory import global_variables
from core.operators import eval_expression
from core.variable import Variable
from utils.interpreter_util import get_function_parameters, normalize_name
from enums.type import Type


def validate_file(filename: str) -> None:
    if not (os.path.isfile(filename) and os.access(filename, os.R_OK) and filename.endswith(".lo")):
        raise FileNotFoundError(filename)


def validate_args() -> str:
    args = sys.argv[1:]
    if len(args) != 1:
        raise FileNotFoundError("Invalid number of arguments")
    validate_file(args[0])
    return args[0]


def load_file_content(filename: str) -> None:
    with open(filename, "r") as f:
        lines = f.readlines()

    statements = group_statements(lines)

    for stmt in statements:
        interpret_statement(stmt)


def group_statements(lines: List[str]) -> List[str]:
    statements = []
    buffer = ""
    open_parens = 0

    for line in lines:
        stripped = line.strip()

        if not stripped or stripped.startswith("//") or stripped.startswith("#"):
            continue

        open_parens += stripped.count("(")
        open_parens -= stripped.count(")")

        buffer += stripped + " "

        if open_parens == 0:
            for token in tokenize(buffer):
                if token:
                    statements.append(token)
            buffer = ""

    if buffer:
        for token in tokenize(buffer):
            if token:
                statements.append(token)

    return statements


def tokenize(data: str) -> List[str]:
    return [t.strip() for t in data.split(";")]


def interpret_statement(data: str) -> None:
    if handle_function_call(data):
        return
    handle_variable_assignment(data)


def handle_function_call(data: str) -> bool:
    if "(" not in data or ")" not in data:
        return False

    assignment = False
    call_expr = data

    if "=" in data:
        left, right = data.split("=", 1)
        left = left.strip()
        type_candidate = left.split(" ", 1)[0]

        if Type.is_valid_type(type_candidate):
            assignment = True
            call_expr = right.strip()

    function_name = normalize_name(call_expr.split("(", 1)[0])
    function = CORE_FUNCTIONS.get(function_name)
    if not function:
        return False

    params = get_function_parameters(call_expr)
    result = function(params)

    if assignment and result is not None:
        left = data.split("=", 1)[0]
        type_name, var_name = left.strip().split(" ", 1)
        register_variable(var_name, type_name, result)

    return True


def handle_variable_assignment(data: str) -> bool:
    if " = " not in data:
        return False

    left, right = data.split(" = ", 1)
    right = eval_expression(right.strip())

    parts = left.strip().split(" ", 1)

    if len(parts) == 2 and Type.is_valid_type(parts[0]):
        type_name, var_name = parts
        register_variable(var_name, type_name, right)
        return True

    var_name = normalize_name(left)
    if var_name not in global_variables:
        raise NameError(f"Variable '{var_name}' not defined")

    global_variables[var_name].set_value(right)
    return True


def register_variable(var_name: str, type_name: str, value) -> None:
    name = normalize_name(var_name)
    variable = Variable(name=name, v_type=Type[type_name.upper()])
    variable.set_value(value)
    global_variables[name] = variable


if __name__ == "__main__":
    filename = validate_args()
    load_file_content(filename)
