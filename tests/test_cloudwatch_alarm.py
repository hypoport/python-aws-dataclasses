import datetime

import pytest
from dateutil.tz import tzutc, tzoffset

from aws_dataclasses.cloudwatch_alarm import CloudWatchAlarm
from aws_dataclasses.cloudwatch_event import CloudWatchEvent

from .util import get_event_dict


@pytest.fixture(scope="module")
def cloudwatch_alarm_raw():
    return get_event_dict("cloudwatch_alarm.json")


@pytest.fixture(scope="module")
def cloudwatch_alarm(cloudwatch_alarm_raw):
    return CloudWatchAlarm.from_json(cloudwatch_alarm_raw)


def test_toplevel_items(cloudwatch_alarm):
    evt = cloudwatch_alarm
    assert evt.alarm_name == "TestAlarm"
    assert evt.alarm_description == "zZt ist der JWT  für den Abruf im PM nur 30min gültig => dies kann zu 403 führen"
    assert evt.new_state_reason == "Threshold Crossed: 1 out of the last 1 datapoints " \
                                   "[3.0 (05/09/18 07:09:00)] was greater than the threshold (0.0) " \
                                   "(minimum 1 datapoint for OK -> ALARM transition)."
    assert evt.new_state_value == "ALARM"
    assert evt.old_state_value == "INSUFFICIENT_DATA"
    assert evt.state_change_time == datetime.datetime(2018, 9, 5, 7, 14, 44, 13000, tzinfo=tzoffset(None, 0))
    assert evt.trigger is not None


def test_trigger_items(cloudwatch_alarm):
    evt = cloudwatch_alarm.trigger
    assert evt.metric_name == "4XXError"
    assert evt.namespace == "AWS/ApiGateway"
    assert evt.period == 300
