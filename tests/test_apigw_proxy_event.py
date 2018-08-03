import pytest

from aws_dataclasses.http_proxy_event import ApiGwProxyEvent

from .util import get_event_dict


@pytest.fixture(scope="module")
def apigw_proxy_event_raw():
    return get_event_dict("apigw-proxy-event.json")


@pytest.fixture(scope="module")
def apigw_proxy_event(apigw_proxy_event_raw):
    return ApiGwProxyEvent.from_event(apigw_proxy_event_raw)


def test_apigw_proxy_event(apigw_proxy_event):
    evt = apigw_proxy_event
    assert evt.path == "/path/to/resource"
    assert evt.http_method == "POST"
    assert evt.request_context.account_id == "123456789012"
