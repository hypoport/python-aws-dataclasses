from datetime import datetime
from typing import Dict, List

import arrow
from dataclasses import dataclass, InitVar, field

from aws_dataclasses.base import GenericDataClass, EventClass


@dataclass
class S3Object(GenericDataClass):
    etag: str = field(init=False, default=None)
    sequencer: str = field(default=None)
    key: str = field(default=None)
    size: float = field(default=None)
    eTag: InitVar[str] = field(repr=False, default=None)

    def __post_init__(self, eTag: str):
        self.etag = eTag


@dataclass
class S3Bucket(GenericDataClass):
    arn: str = field(default=None)
    name: str = field(default=None)
    owner_identity: str = field(init=False, default=None)
    ownerIdentity: InitVar[str] = field(repr=False, default=None)

    def __post_init__(self, ownerIdentity: str):
        self.owner_identity = ownerIdentity


@dataclass
class S3(GenericDataClass):
    object: S3Object
    bucket: S3Bucket
    configuration_id: str = field(init=False, default=None)
    s3_schemaversion: str = field(init=False, default=None)
    configurationId: InitVar[str] = field(repr=False, default=None)
    s3SchemaVersion: InitVar[str] = field(repr=False, default=None)

    def __post_init__(self, configurationId: str, s3SchemaVersion: str):
        self.configuration_id = configurationId
        self.s3_schemaversion = s3SchemaVersion
        self.object = S3Object.from_json(self.object)
        self.bucket = S3Bucket.from_json(self.bucket)


@dataclass
class S3Record(GenericDataClass):
    s3: S3
    event_version: str = field(init=False)
    event_source: str = field(init=False)
    event_time: datetime = field(init=False)
    event_name: str = field(init=False)
    response_elements: Dict[str, str] = field(init=False, default=None)
    aws_region: str = field(init=False)
    user_identity: Dict[str, str] = field(init=False, default=None)
    request_params: Dict[str, str] = field(init=False, default=None)
    eventVersion: InitVar[str] = field(repr=False, default=None)
    eventTime: InitVar[str] = field(repr=False, default=None)
    requestParameters: InitVar[Dict[str, str]] = field(repr=False, default=None)
    responseElements: InitVar[Dict[str, str]] = field(repr=False, default=None)
    awsRegion: InitVar[str] = field(repr=False, default=None)
    eventName: InitVar[str] = field(repr=False, default=None)
    userIdentity: InitVar[Dict[str, str]] = field(repr=False, default=None)
    eventSource: InitVar[str] = field(repr=False, default=None)

    def __post_init__(self, eventVersion: str, eventTime: str, requestParameters: Dict[str, str],
                      responseElements: Dict[str, str], awsRegion: str, eventName: str, userIdentity: Dict[str, str],
                      eventSource: str):
        self.event_name = eventName
        self.event_time = arrow.get(eventTime).datetime
        self.event_source = eventSource
        self.event_version = eventVersion
        self.response_elements = responseElements
        self.aws_region = awsRegion
        self.request_params = requestParameters
        self.user_identity = userIdentity
        self.s3 = S3.from_json(self.s3)


@dataclass
class S3Event(EventClass):
    records: List[S3Record] = field(init=False)
    first_record: S3Record = field(init=False)
    Records: InitVar[List[Dict]] = field(repr=False, default=[])

    def __post_init__(self, Records: List[Dict]):
        self.records = [S3Record.from_json(item) for item in Records]
        self.first_record = self.records[0]
