import datetime

import pytest
from dateutil.tz import tzutc

from aws_dataclasses.kinesis_datastream_event import (
    KinesisDataStreamEvent,
    KinesisSingleRecord,
)

from .util import get_event_dict


@pytest.fixture(scope="module")
def kinesis_datastream_event_raw():
    return get_event_dict("kinesis-datastream-event.json")


@pytest.fixture(scope="module")
def kinesis_datastream_event(kinesis_datastream_event_raw):
    return KinesisDataStreamEvent.from_event(kinesis_datastream_event_raw)


def test_kinesis_datastream_record(kinesis_datastream_event):
    assert kinesis_datastream_event.first_record is not None
    record = kinesis_datastream_event.first_record
    assert record.event_version == "1.0"
    assert record.event_source == "aws:kinesis"


def test_kinesis_datastream(kinesis_datastream_event):
    assert kinesis_datastream_event.first_record.kinesis is not None
    kinesis: KinesisSingleRecord = kinesis_datastream_event.first_record.kinesis
    assert kinesis.data == "SGVsbG8sIHRoaXMgaXMgYSB0ZXN0Lg=="
    assert kinesis.approximate_arrival_timestamp == 1545084650.987


def test_can_handle_missing_fields(kinesis_datastream_event_raw):
    kinesis_record = kinesis_datastream_event_raw["Records"][0]["kinesis"]
    kinesis_record.pop("partitionKey")
    res = KinesisSingleRecord.from_json(kinesis_record)
    assert res.partition_key is None


def test_can_handle_extra_fields(kinesis_datastream_event_raw):
    kinesis_record = kinesis_datastream_event_raw["Records"][0]["kinesis"]
    kinesis_record["TestAttr"] = 1234
    res = KinesisSingleRecord.from_json(kinesis_record)
    assert res is not None
