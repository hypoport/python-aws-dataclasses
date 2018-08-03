from collections import namedtuple
from typing import Dict

HeaderDict = namedtuple("HeaderDict", ['key', 'value'])


def parse_headers(headers):
    return {hdr_name: HeaderDict(header[0].get("key", None),
                                 header[0].get("value", None)) for hdr_name, header in headers.items()}


class CfConfig:
    def __init__(self, distribution_id: str, request_id: str):
        self._distribution_id = distribution_id
        self._request_id = request_id

    @classmethod
    def from_json(cls, config):
        return cls(config["distributionId"],
                   config["requestId"])

    @property
    def distribution_id(self) -> str:
        return self._distribution_id

    @property
    def request_id(self) -> str:
        return self._request_id


class CfRequest:
    def __init__(self, client_ip: str,
                 querystring: str,
                 uri: str,
                 method: str,
                 headers: Dict[str, HeaderDict],
                 origin):
        self._client_ip = client_ip
        self._querystring = querystring
        self._uri = uri
        self._http_method = method
        self._headers = headers
        self._origin = origin

    @classmethod
    def from_json(cls, request):
        return cls(request["clientIp"],
                   request["querystring"],
                   request["uri"],
                   request["method"],
                   parse_headers(request["headers"]),
                   request.get("origin", None))

    @property
    def client_ip(self) -> str:
        return self._client_ip

    @property
    def querystring(self) -> str:
        return self._querystring

    @property
    def uri(self) -> str:
        return self._uri

    @property
    def http_method(self) -> str:
        return self._http_method

    @property
    def headers(self) -> Dict[str, HeaderDict]:
        return self._headers

    @property
    def origin(self):
        return self._origin


class CfResponse:
    def __init__(self, status: str, status_description: str, headers: Dict[str, HeaderDict]):
        self._status = status
        self._status_description = status_description
        self._headers = headers

    @classmethod
    def from_json(cls, response):
        if response is not None:
            return cls(response["status"],
                       response["statusDescription"],
                       parse_headers(response["headers"]))

    @property
    def status(self) -> str:
        return self._status

    @property
    def status_description(self) -> str:
        return self._status_description

    @property
    def headers(self) -> Dict[str, HeaderDict]:
        return self._headers


class CfRecord:
    def __init__(self, config: CfConfig,
                 request: CfRequest,
                 response: CfResponse):
        self._config = config
        self._request = request
        self._response = response

    @classmethod
    def from_json(cls, cf):
        return cls(CfConfig.from_json(cf["config"]),
                   CfRequest.from_json(cf["request"]),
                   CfResponse.from_json(cf.get("response", None)))

    @property
    def config(self) -> CfConfig:
        return self._config

    @property
    def request(self) -> CfRequest:
        return self._request

    @property
    def response(self) -> CfResponse:
        return self._response


class CloudfrontEvent:
    def __init__(self, records: [CfRecord]):
        self._records = records

    @classmethod
    def from_event(cls, event):
        return cls([CfRecord.from_json(record["cf"]) for record in event["Records"]])

    @property
    def records(self) -> [CfRecord]:
        return self._records

    @property
    def first_record(self) -> CfRecord:
        return self._records[0]
