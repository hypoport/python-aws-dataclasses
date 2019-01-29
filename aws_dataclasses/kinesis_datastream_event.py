from collections import namedtuple
from base64 import b64decode
from typing import Dict, List

import arrow
from dataclasses import dataclass, field, InitVar

from aws_dataclasses.base import GenericDataClass, EventClass


@dataclass
class KinesisSingleRecord(GenericDataClass):
    kinesis_schema_version: str = field(init=False)
    approximate_arrival_timestamp: float = field(init=False)
    partition_key: str = field(init=False)
    sequence_number: str = field(init=False)
    data: str = field(init=True)

    kinesisSchemaVersion: InitVar[str] = field(repr=False, default=None)
    partitionKey: InitVar[str] = field(repr=False, default=None)
    sequenceNumber: InitVar[str] = field(repr=False, default=None)
    approximateArrivalTimestamp: InitVar[float] = field(repr=False, default=None)

    def __post_init__(
        self,
        kinesisSchemaVersion: str,
        partitionKey: str,
        sequenceNumber: str,
        approximateArrivalTimestamp: str,
    ):
        self.kinesis_schema_version = kinesisSchemaVersion
        self.partition_key = partitionKey
        self.sequence_number = sequenceNumber
        self.approximate_arrival_timestamp = approximateArrivalTimestamp

    @property
    def string_data(self):
        return b64decode(self.data.encode("utf-8")).decode("utf-8")


@dataclass
class KinesisRecord(GenericDataClass):
    event_source: str = field(init=False)
    kinesis: KinesisSingleRecord = field(init=True)
    event_version: str = field(init=False)
    event_source_arn: str = field(init=False)
    eventSource: InitVar[str] = field(repr=False, default=None)
    eventVersion: InitVar[str] = field(repr=False, default=None)
    eventID: InitVar[str] = field(repr=False, default=None)
    eventName: InitVar[str] = field(repr=False, default=None)
    eventSourceARN: InitVar[str] = field(repr=False, default=None)
    awsRegion: InitVar[str] = field(repr=False, default=None)
    invokeIdentityArn: InitVar[str] = field(repr=False, default=None)

    def __post_init__(
        self,
        eventSource: str,
        eventVersion: str,
        eventID: str,
        eventName: str,
        eventSourceARN: str,
        awsRegion: str,
        invokeIdentityArn: str,
    ):
        self.event_source = eventSource
        self.event_version = eventVersion
        self.event_source_arn = eventSourceARN
        self.kinesis = KinesisSingleRecord.from_json(self.kinesis)


@dataclass
class KinesisDataStreamEvent(EventClass):
    records: List[KinesisRecord] = field(init=False)
    first_record: KinesisRecord = field(init=False)
    Records: InitVar[List] = field(repr=False, default=[])

    def __post_init__(self, Records: List):
        self.records = [KinesisRecord.from_json(record) for record in Records]
        self.first_record = self.records[0]
