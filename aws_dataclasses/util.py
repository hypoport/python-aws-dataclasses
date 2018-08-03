import warnings
from typing import Dict


def handle_nonexisting_fields(item: Dict, cls):
    out = {}
    for k, v in item.items():
        if k not in cls.__dataclass_fields__:
            warnings.warn(f"Found field \"{k}\" in input, which is not part of dataclass \"{cls.__name__}\"",
                          RuntimeWarning)
        else:
            out[k] = v
    return out
