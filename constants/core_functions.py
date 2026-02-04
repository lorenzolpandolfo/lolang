from core.io import println_impl, print_impl
from core.random import randint_impl

CORE_FUNCTIONS = {
    "println": println_impl,
    "print": print_impl,
    "randint": randint_impl
}
