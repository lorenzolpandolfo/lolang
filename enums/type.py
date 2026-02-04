from enum import Enum
from typing import Any
from unittest import case

from utils.log import log


class Type(Enum):
    STRING = "string"
    BOOLEAN = "boolean"
    FLOAT = "float"
    INT = "int"

    @classmethod
    def is_valid_type(cls, v_type: str) -> bool:
        return v_type.upper() in cls.__members__

    def parse_value_to_type(self, v_value: str) -> Any:
        match self.value:
            case self.STRING.value:
                return v_value.replace('"', '')

            case self.INT.value:
                return int(v_value)

            case self.FLOAT.value:
                return float(v_value)

            case self.BOOLEAN.value:
                return bool(v_value)
                # return v_value.lower() == "true"

            case _:
                return None

    def parse_to_python_type(self):

        match self.value:
            case self.STRING.value:
                return str
            case self.BOOLEAN.value:
                return bool
            case self.FLOAT.value:
                return float
            case self.INT.value:
                return int
            case _:
                return None
