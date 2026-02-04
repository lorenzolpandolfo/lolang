from datetime import datetime
from typing import List


def now_impl(params: List[str]):

    if params is None or len(params) == 0:
       return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return datetime.now().strftime(params[0])
