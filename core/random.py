from collections.abc import Generator
import time
from typing import List

from utils.log import log


def _lcg(modulus: int, a: int, c: int, seed: int) -> Generator[int, None, None]:
    while True:
        seed = (a * seed + c) % modulus
        yield seed

rng = _lcg(2 ** 32, 1664525, 1013904223, time.time_ns())

def randint_impl(params: List[int]):
    a = params[0]
    b = params[1]
    c = a + (next(rng) % (b - a + 1))
    return c

