from collections import namedtuple
from typing import Dict, List, Optional

from dataclasses import InitVar, field, dataclass

from util import GenericDataClass

KVPair = namedtuple("KVPair", ['key', 'value'])


def _parse_headers(headers) -> Dict[str, List[KVPair]]:
    out = {}
    for hdr_name, header_list in headers.items():
        out[hdr_name] = [KVPair(header.get("key"), header.get("value")) for header in header_list]
    return out


@dataclass
class CloudFrontConfig(GenericDataClass):
    distribution_id: str = field(init=False)
    request_id: str = field(init=False)
    distributionId: InitVar[str] = field(repr=False, default=None)
    requestId: InitVar[str] = field(repr=False, default=None)

    def __post_init__(self, distributionId: str, requestId: str):
        self.request_id = requestId
        self.distribution_id = distributionId


@dataclass
class CloudFrontfRequest(GenericDataClass):
    querystring: str
    uri: str
    method: str
    headers: Dict[str, List[KVPair]]
    origin: str = field(default=None)
    client_ip: str = field(init=False)
    clientIp: InitVar[str] = field(repr=False, default=None)

    def __post_init__(self, clientIp: str):
        self.client_ip = clientIp
        self.headers = _parse_headers(self.headers)


@dataclass
class CloudFrontResponse(GenericDataClass):
    status: str
    status_description: str = field(init=False)
    headers: Dict[str, List[KVPair]]
    statusDescription: InitVar[str] = field(repr=False, default=None)

    def __post_init__(self, statusDescription: str):
        self.status_description = statusDescription
        self.headers = _parse_headers(self.headers)


@dataclass
class CloudFrontRecord(GenericDataClass):
    config: CloudFrontConfig
    request: Optional[CloudFrontfRequest] = field(default=None)
    response: Optional[CloudFrontResponse] = field(default=None)

    def __post_init__(self):
        self.config = CloudFrontConfig(**self.config)
        self.request = CloudFrontfRequest(**self.request) if self.request is not None else self.request
        self.response = CloudFrontResponse(**self.response) if self.response is not None else self.response


@dataclass
class CloudFrontEvent(GenericDataClass):
    records: List[CloudFrontRecord] = field(init=False)
    first_record: CloudFrontRecord = field(init=False)
    Records: InitVar[List[Dict]] = field(repr=False, default=[])

    def __post_init__(self, Records: List[Dict]):
        self.records = [CloudFrontRecord(**record["cf"]) for record in Records]
        self.first_record = self.records[0]

    @classmethod
    def from_event(cls, event):
        return cls.from_json(event)
