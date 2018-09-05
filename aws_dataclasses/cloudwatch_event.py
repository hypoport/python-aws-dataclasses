from datetime import datetime
from typing import Dict, List, Any

import arrow
from dataclasses import dataclass

from aws_dataclasses.base import EventClass


@dataclass
class CloudWatchEvent(EventClass):
    version: str
    id: str
    detail_type: str
    source: str
    account: str
    time: datetime
    region: str
    resources: List[str]
    detail: Dict[str, Any]

    def __post_init__(self):
        self.time = arrow.get(self.time).datetime
