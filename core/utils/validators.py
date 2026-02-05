from typing import Callable


def validate_empty_params(func: Callable) -> Callable:
    def wrapper(params, *args, **kwargs):
        if len(params) == 0:
            return None

        return func(params, *args, **kwargs)
    return wrapper

def validate_first_param_list(func: Callable) -> Callable:
    def wrapper(params, *args, **kwargs):
        if not isinstance(params[0], list):
            return None

        return func(params, *args, **kwargs)
    return wrapper

def validate_list_or_string(func: Callable) -> Callable:
    def wrapper(params, *args, **kwargs):
        if not isinstance(params[0], list) and not isinstance(params[0], str):
            return params[0]

        return func(params, *args, **kwargs)
    return wrapper