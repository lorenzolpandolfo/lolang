from typing import List

from core.utils.validators import validate_empty_params


@validate_empty_params
def abs_impl(params: List[str]) -> float:
    return abs(float(params[0]))

@validate_empty_params
def round_impl(params: List[str]) -> float:
    return round(float(params[0]))