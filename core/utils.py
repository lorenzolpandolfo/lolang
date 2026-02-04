from typing import List, Any

from utils.validators import validate_empty_params


def typeof_impl(params: List[Any]) -> str:
    if len(params) == 0:
        return ""
    return type(params[0])

@validate_empty_params
def evaluate_impl(params: List[str]) -> float:
    return eval(*params)
