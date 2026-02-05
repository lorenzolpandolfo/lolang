from time import sleep
from typing import List, Any


def sleep_impl(params: List[Any]) -> None:
    if len(params) == 0:
        return

    sleep(params[0])