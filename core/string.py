from typing import List


def len_impl(params: List[str]) -> int:

    if params is None or len(params) == 0:
        return 0

    return len(params[0])


def upper_impl(params: List[str]) -> str:
    if params is None or len(params) == 0:
        return ""

    return params[0].upper()


def lower_impl(params: List[str]) -> str:
    if params is None or len(params) == 0:
        return ""

    return params[0].lower()

