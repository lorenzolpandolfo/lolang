from typing import List

from core.utils.validators import validate_empty_params


@validate_empty_params
def length_impl(params: List[str]) -> int:
    return len(params[0])


@validate_empty_params
def upper_impl(params: List[str]) -> str:
    return params[0].upper()


@validate_empty_params
def lower_impl(params: List[str]) -> str:
    return params[0].lower()

@validate_empty_params
def contains_impl(params: List[str]) -> bool:
    return params[0] in params[1]
