from typing import Callable


def validate_empty_params(func: Callable) -> Callable:
    def wrapper(params, *args, **kwargs):
        if len(params) == 0:
            return None

        return func(params, *args, **kwargs)
    return wrapper