import os
import sys
from typing import List

from constants.core_functions import CORE_FUNCTIONS
from core.memory import global_variables
from core.operators import eval_expression
from core.objects.variable import Variable
from utils.interpreter_util import get_function_parameters, normalize_name
from enums.type import Type
from utils.log import log


def _validate_file(file: str) -> None:
    if not (os.path.isfile(file) and os.access(file, os.R_OK) and file.endswith(".lo")):
        raise FileNotFoundError(file)


def _validate_args() -> str:
    args = sys.argv[1:]
    if len(args) != 1:
        raise FileNotFoundError("Invalid number of arguments")
    _validate_file(args[0])
    return args[0]


def load_file_content(filename: str) -> None:
    with open(filename, "r") as f:
        lines = f.readlines()

    statements = group_statements(lines)

    i = 0
    while i < len(statements):
        stmt = statements[i]

        if stmt.startswith("if"):
            i = handle_if_statement(statements, i)
        elif stmt.startswith("while"):
            i = handle_while_statement(statements, i)
        elif stmt.startswith("for"):
            i = handle_for_statement(statements, i)
        else:
            interpret_statement(stmt)
            i += 1

def group_statements(lines: List[str]) -> List[str]:
    statements = []
    buffer = ""
    open_parens = 0

    for line in lines:
        stripped = line.strip()

        if not stripped or stripped.startswith("//") or stripped.startswith("#"):
            continue

        stripped = stripped.replace("} else {", "}\nelse {")

        for part in stripped.splitlines():
            part = part.strip()

            if part == "}":
                if buffer:
                    statements.append(buffer.strip())
                    buffer = ""
                statements.append("}")
                continue

            open_parens += part.count("(")
            open_parens -= part.count(")")

            buffer += part + " "

            # 🔑 só fecha o statement se NÃO estivermos esperando um {
            if open_parens == 0 and not buffer.strip().startswith(("for ", "if ", "while ")) or buffer.strip().endswith("{"):
                statements.append(buffer.strip())
                buffer = ""

    if buffer:
        statements.append(buffer.strip())

    return statements



def collect_block(statements: List[str], start: int):
    block = []
    depth = 0
    i = start

    while i < len(statements):
        stmt = statements[i]

        if stmt.endswith("{"):
            depth += 1

        if stmt == "}":
            if depth == 0:
                return block, i + 1
            depth -= 1

        block.append(stmt)
        i += 1

    raise SyntaxError("Missing '}'")


def handle_if_statement(statements: List[str], index: int) -> int:
    line = statements[index]

    condition = line[2:].strip()

    if not condition.endswith("{"):
        raise SyntaxError("Expected '{' after if condition")

    condition = condition[:-1].strip()
    result = eval_expression(condition)

    true_block, i = collect_block(statements, index + 1)

    false_block = []
    if i < len(statements) and statements[i].startswith("else"):
        else_line = statements[i]

        if not else_line.endswith("{"):
            raise SyntaxError("Expected '{' after else")

        false_block, i = collect_block(statements, i + 1)

    block = true_block if result else false_block
    execute_block(block)
    return i

def handle_while_statement(statements: List[str], index: int) -> int:
    line = statements[index]
    condition = line[5:].strip()

    if not condition.endswith("{"):
        raise SyntaxError("Expected '{' after while condition")

    condition = condition[:-1].strip()
    block, end = collect_block(statements, index + 1)

    while eval_expression(condition):
        execute_block(block)

    return end

def handle_for_statement(statements: List[str], index: int) -> int:
    line = statements[index]
    header = line[3:].strip()


    if not header.endswith("{"):
        raise SyntaxError("Expected '{' after for header")

    header = header[:-1].strip()

    try:
        init, condition, increment = [p.strip() for p in header.split(";")]
    except ValueError:
        raise SyntaxError("Invalid for syntax")

    block, end = collect_block(statements, index + 1)
    interpret_statement(init)

    while eval_expression(condition):
        execute_block(block)
        interpret_statement(increment)

    return end


def execute_block(statements: List[str]) -> None:
    i = 0
    while i < len(statements):
        stmt = statements[i]

        if stmt.startswith("if"):
            i = handle_if_statement(statements, i)
        else:
            interpret_statement(stmt)
            i += 1


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
    filename = _validate_args()
    load_file_content(filename)
