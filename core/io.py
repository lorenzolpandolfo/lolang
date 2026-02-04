from typing import List, Callable

from enums.color import Color
from utils.interpreter_util import sanitize_parameter
from utils.log import log


def validate_params(func: Callable) -> Callable:
    def wrapper(params, *args, **kwargs):
        if not params:
            return None

        return func(params, *args, **kwargs)

    return wrapper


def println_impl(params: List[str]) -> None:
    if not params:
        print()
        return

    content = params[0]

    if len(params) == 1:
        print(content)
        return

    color = params[1]
    color = sanitize_parameter(color.upper())

    try:
        color = Color[color]
        print(f"{color}{content}{Color.ENDC}")

    except KeyError:
        raise ValueError(f"[println] invalid color {color}. Must be RED, GREEN, YELLOW, BLUE, MAGENTA or CYAN.")


@validate_params
def print_impl(params: List[str]) -> None:
    print(params[0], end="")
