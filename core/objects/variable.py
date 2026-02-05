from typing import Any

from core.enums.type import Type


class Variable:
    def __init__(self, name: str, v_type: Type) -> None:
        self.name = name
        self.type = v_type
        self.value = None

    def set_value(self, v_value: Any) -> None:
        v_in_py_type = self.type.parse_value_to_type(v_value)


        if not isinstance(v_in_py_type, self.type.parse_to_python_type()):
            raise TypeError(
                f"[Error] Variable {self.name} has type {self.type} but value was set to {v_value} of type {type(v_value)}")

        self.value = v_in_py_type
