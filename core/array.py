from typing import Any, List

from utils.log import log
from utils.validators import validate_empty_params, validate_first_param_list, validate_list_or_string


@validate_empty_params
@validate_first_param_list
def push_impl(params: List[Any]) -> list:
    if not isinstance(params[0], list):
        raise ValueError("Push requires a list in first parameter")

    array: list = params[0]

    for i in range(len(params)):
        if i == 0:
            continue

        param = params[i]
        array.append(param)
    return array

@validate_empty_params
@validate_first_param_list
def pop_impl(params: List[Any]) -> list:
    array: list = params[0]
    index: int = params[1]

    array.pop(index)
    return array


@validate_empty_params
@validate_list_or_string
def reverse_impl(parms: List[Any]) -> Any:
    obj = parms[0]
    return obj[::-1]