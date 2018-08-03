import pytest

from aws_dataclasses.cf_event import CloudfrontEvent

from .util import get_event_dict


@pytest.fixture(scope="module")
def cf_request_event_raw():
    return get_event_dict("cf_request_event.json")


@pytest.fixture(scope="module")
def cf_response_event_raw():
    return get_event_dict("cf_response_event.json")


@pytest.fixture(scope="module")
def cf_request_event(cf_request_event_raw):
    return CloudfrontEvent.from_event(cf_request_event_raw)


@pytest.fixture(scope="module")
def cf_response_event(cf_response_event_raw):
    return CloudfrontEvent.from_event(cf_response_event_raw)


def test_request(cf_request_event):
    evt = cf_request_event.first_record
    assert evt.config.request_id == "MRVMF7KydIvxMWfJIglgwHQwZsbG2IhRJ07sn9AkKUFSHS9EXAMPLE=="
    assert evt.response is None
    assert evt.request.querystring == "size=large"


def test_response(cf_response_event):
    evt = cf_response_event.first_record
    assert evt.config.request_id == "xGN7KWpVEmB9Dp7ctcVFQC4E-nrcOcEKS3QyAez--06dV7TEXAMPLE=="
    assert evt.response.status == "200"
    assert evt.request.client_ip == "2001:0db8:85a3:0:0:8a2e:0370:7334"
