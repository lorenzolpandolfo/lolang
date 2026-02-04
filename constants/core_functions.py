from datetime import datetime
from random import choice
from time import sleep

from core.io import println_impl, print_impl, input_impl
from core.random import randint_impl
from core.string import len_impl, upper_impl, lower_impl
from core.time import now_impl

CORE_FUNCTIONS = {
    "println": println_impl,
    "print": print_impl,
    "randint": randint_impl,
    "input": input_impl,
    "len": len_impl,
    "upper": upper_impl,
    "lower": lower_impl,
    # "contains": str.__contains__,
    # "abs": abs,
    # "round": round,
    "now": now_impl,
    # "sleep": sleep,
    # "choice": choice,
    # "type": type

}
