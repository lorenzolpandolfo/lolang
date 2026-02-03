from typing import List


def get_function_parameters(f: str) -> List[str]:
    args: List[str] = f.split("(")
    params: List[str] = args[1].strip(")").split(",")
    return params

def sanitize_parameter(param: str) -> str:
    return param.strip().replace('"', "")