import datetime

from enums.color import Color
from time import time

def log(*args, **kwargs) -> None:
    msg = " ".join(map(str, args))
    extra = " ".join(f"{k}={v}" for k, v in kwargs.items())
    time = datetime.datetime.now().strftime("%H:%M:%S:%f")
    print(f"{time} {Color.RED}[DEBUG]{Color.ENDC} {msg} {extra}".strip())
