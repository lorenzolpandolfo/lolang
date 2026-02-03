import os
import sys
from typing import List

import core.io as lolang_core_io
from utils.interpreter_util import get_function_parameters


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

    params: List[str] = get_function_parameters(data)

    if data.__contains__("println("):
        lolang_core_io.println_impl(params)

    if data.__contains__("print("):
        lolang_core_io.print_impl(params)



if __name__ == "__main__":
    validate_args()
    load_file_content()
