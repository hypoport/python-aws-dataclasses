import pytest

from aws_dataclasses.s3_event import S3Event
from .util import get_event_dict


@pytest.fixture(scope="module")
def s3_event_raw():
    return get_event_dict("s3-event.json")


@pytest.fixture(scope="module")
def s3_event(s3_event_raw):
    return S3Event.from_event(s3_event_raw)


def test_s3_event_contains_s3(s3_event):
    evt = s3_event
    assert evt.first_record.s3 is not None
    s3 = evt.first_record.s3
    assert s3.configuration_id == "testConfigRule"
    assert s3.s3_schemaversion == "1.0"


def test_s3_event_contains_object(s3_event):
    evt = s3_event
    assert evt.first_record.s3.object is not None
    obj = evt.first_record.s3.object
    assert obj.key == "HappyFace.jpg"
    assert obj.size == 1024
    assert obj.etag == "0123456789abcdef0123456789abcdef"
    assert obj.sequencer == "0A1B2C3D4E5F678901"


def test_s3_event_contains_bucket(s3_event):
    evt = s3_event
    assert evt.first_record.s3.bucket is not None
    bucket = evt.first_record.s3.bucket
    assert bucket.name == "sourcebucket"
    assert bucket.arn == "arn:aws:s3:::mybucket"


def test_s3_event_contains_record(s3_event):
    evt = s3_event
    assert evt.first_record is not None
    record = evt.first_record
    assert record.event_time.strftime('%Y-%m-%dT%H:%M:%S%z') == "1970-01-01T00:00:00+0000"
    assert record.event_version == "2.0"
    assert record.aws_region == "us-east-1"
    assert record.event_name == "ObjectCreated:Put"
