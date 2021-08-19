import copy
import datetime

import pytest
from dateutil.tz import tzutc

from aws_dataclasses.sns_event import SnsEvent, SnsMessage

from .util import get_event_dict


@pytest.fixture(scope="module")
def sns_event_raw():
    return get_event_dict("sns-event.json")


@pytest.fixture(scope="module")
def sns_event(sns_event_raw):
    return SnsEvent.from_event(sns_event_raw)


def test_sns_record(sns_event):
    assert sns_event.first_record is not None
    evt = sns_event.first_record
    assert evt.event_version == "1.0"
    assert evt.event_source == "aws:sns"


def test_sns(sns_event):
    assert sns_event.first_record.sns is not None
    sns = sns_event.first_record.sns
    assert sns.message == "Hello from SNS!"
    assert sns.timestamp == datetime.datetime(1970, 1, 1, 0, 0, 12, tzinfo=tzutc())
    assert int(sns.timestamp.timestamp()) == 12
    assert sns.topic_arn == "arn:aws:sns:EXAMPLE"
    assert sns.signature == "EXAMPLE"


def test_message_attributes(sns_event):
    msg_attr = sns_event.first_record.sns.message_attributes
    assert msg_attr.get("Test").value == "TestString"
    assert msg_attr.get("Test").type == "String"


def test_can_handle_missing_fields(sns_event_raw):
    sns = copy.deepcopy(sns_event_raw["Records"][0]["Sns"])
    sns.pop("MessageAttributes")
    res = SnsMessage.from_json(sns)
    assert res.message_attributes is None


def test_can_handle_extra_fields(sns_event_raw):
    sns = sns_event_raw["Records"][0]["Sns"]
    sns["TestAttr"] = 1234
    res = SnsMessage.from_json(sns)
    assert res is not None
