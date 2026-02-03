from typing import Optional, List

from enums.color import Color
from utils.interpreter_util import sanitize_parameter

def println_impl(params: List[str]) -> None:

    if params is None:
        return

    content: str = sanitize_parameter(params[0])

    if len(params) == 1:
        print(content)
        return

    color_param: str = sanitize_parameter(params[1].upper())
    try:
        c: Color = Color[color_param]
        print(f"{c}{content}{Color.ENDC}")

    except Exception as e:
        raise ValueError(f"[println] invalid color {color_param}. Must be RED, GREEN, YELLOW, BLUE, MAGENTA or CYAN.")


def print_impl(params: List[str]) -> None:
    content = sanitize_parameter(params[0])
    print(content, end="")

