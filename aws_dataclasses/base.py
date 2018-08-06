import json
import warnings
from typing import Union, Dict

from dataclasses import dataclass


def _handle_nonexisting_fields(item: Dict, cls):
    out = {}
    for k, v in item.items():
        if k not in cls.__dataclass_fields__:
            warnings.warn(f"Found field \"{k}\" in input, which is not part of dataclass \"{cls.__name__}\"",
                          RuntimeWarning)
        else:
            out[k] = v
    return out


@dataclass
class GenericDataClass:
    @classmethod
    def from_json(cls, input: Union[str, Dict]):
        if isinstance(input, str):
            input = json.loads(input)
        input = _handle_nonexisting_fields(input, cls)
        return cls(**input)


@dataclass
class EventClass(GenericDataClass):
    @classmethod
    def from_event(cls, event):
        return cls.from_json(event)
