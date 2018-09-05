import json
import warnings
from typing import Union, Dict

from dataclasses import dataclass


def _check_fields(item: Dict, cls):
    out = {}
    for k, v in item.items():
        normalized_key = _normalize_key(k)
        if normalized_key not in cls.__dataclass_fields__:
            warnings.warn(f"Found field \"{k}\" in input, which is not part of dataclass \"{cls.__name__}\"",
                          RuntimeWarning)
        else:
            out[normalized_key] = v
    return out


def _normalize_key(identifier: str):
    res = identifier.replace("-", "_")
    return res


@dataclass
class GenericDataClass:
    @classmethod
    def from_json(cls, input: Union[str, Dict]):
        if isinstance(input, str):
            input = json.loads(input)
        input = _check_fields(input, cls)
        return cls(**input)


@dataclass
class EventClass(GenericDataClass):
    @classmethod
    def from_event(cls, event):
        return cls.from_json(event)
