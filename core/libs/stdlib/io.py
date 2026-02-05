from typing import List

from core.enums.color import Color


def _sanitize_parameter(param: str) -> str:
    return param.strip().replace('"', "")


def extract_color(params: List[str]):
    if not params:
        return params, None

    last = params[-1]

    if isinstance(last, str) and last.startswith("&"):
        color_name = _sanitize_parameter(last[1:].upper())
        try:
            return params[:-1], Color[color_name]
        except KeyError:
            raise ValueError(
                f"[print] invalid color {color_name}. Must be RED, GREEN, YELLOW, BLUE, MAGENTA or CYAN."
            )

    return params, None


def print_impl(params: List[str]) -> None:
    params, color = extract_color(params)
    content = "".join(str(p) for p in params)

    if color:
        print(f"{color}{content}{Color.ENDC}", end="")
    else:
        print(content, end="")


def println_impl(params: List[str]) -> None:
    params, color = extract_color(params)
    content = "".join(str(p) for p in params)

    if color:
        print(f"{color}{content}{Color.ENDC}")
    else:
        print(content)

def input_impl(params):
    params, color = extract_color(params)

    prompt = "".join(str(p) for p in params)

    if color:
        return input(f"{color}{prompt}{Color.ENDC}")

    return input(prompt)
