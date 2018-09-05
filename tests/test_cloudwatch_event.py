import datetime

import pytest
from dateutil.tz import tzutc

from aws_dataclasses.cloudwatch_event import CloudWatchEvent

from .util import get_event_dict


@pytest.fixture(scope="module")
def cloudwatch_event_raw():
    return get_event_dict("cloudwatch_event.json")


@pytest.fixture(scope="module")
def cloudwatch_event(cloudwatch_event_raw):
    return CloudWatchEvent.from_event(cloudwatch_event_raw)


def test_toplevel_items(cloudwatch_event):
    evt = cloudwatch_event
    assert evt.version == "0"
    assert evt.id == "9abea4c9-79cd-f4e9-4826-e2bd59590b5c"
    assert evt.detail_type == "Batch Job State Change"
    assert evt.source == "aws.batch"
    assert evt.time == datetime.datetime(2018, 9, 5, 4, 9, 49, tzinfo=tzutc())
    assert evt.region == "eu-central-1"
    assert evt.account == "1234567890"
    assert evt.resources == ["arn:aws:batch:eu-central-1:1234567890:job/6882ce8d-359c-427b-834f-331158e5d093"]
