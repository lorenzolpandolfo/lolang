from core.libs.datetime.datetime import now_impl
from core.libs.stdlib.array import push_impl, pop_impl, reverse_impl
from core.libs.stdlib.io import println_impl, print_impl, input_impl
from core.libs.stdlib.math import abs_impl, round_impl
from core.libs.stdlib.random import randint_impl
from core.libs.stdlib.string import length_impl, upper_impl, lower_impl, contains_impl
from core.libs.stdlib.utils import typeof_impl, evaluate_impl
from core.libs.time.time import sleep_impl

CORE_FUNCTIONS = {
    # string
    "println": println_impl,
    "print": print_impl,
    "input": input_impl,
    "upper": upper_impl,
    "lower": lower_impl,
    "contains": contains_impl,
    "length": length_impl,

    # random
    "randint": randint_impl,

    # time
    "sleep": sleep_impl,

    # datetime
    "now": now_impl,

    # math
    "abs": abs_impl,
    "round": round_impl,

    # utils
    "typeof": typeof_impl,
    "evaluate": evaluate_impl,

    # array
    "push": push_impl,
    "pop": pop_impl,
    "reverse": reverse_impl

}
