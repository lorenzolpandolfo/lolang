from typing import List, Callable
from enums.color import Color


def validate_params(func: Callable) -> Callable:
    def wrapper(params, *args, **kwargs):
        return func(params, *args, **kwargs)
    return wrapper


def sanitize_parameter(param: str) -> str:
    return param.strip().replace('"', "")


def extract_color(params: List[str]):
    if not params:
        return params, None

    last = params[-1]

    if isinstance(last, str) and last.startswith("&"):
        color_name = sanitize_parameter(last[1:].upper())
        try:
            return params[:-1], Color[color_name]
        except KeyError:
            raise ValueError(
                f"[print] invalid color {color_name}. Must be RED, GREEN, YELLOW, BLUE, MAGENTA or CYAN."
            )

    return params, None


@validate_params
def print_impl(params: List[str]) -> None:
    params, color = extract_color(params)
    content = " ".join(str(p) for p in params)

    if color:
        print(f"{color}{content}{Color.ENDC}", end="")
    else:
        print(content, end="")


@validate_params
def println_impl(params: List[str]) -> None:
    params, color = extract_color(params)
    content = " ".join(str(p) for p in params)

    if color:
        print(f"{color}{content}{Color.ENDC}")
    else:
        print(content)
