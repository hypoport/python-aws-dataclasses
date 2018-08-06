import pytest

from aws_dataclasses.http_proxy_event import ApiGwProxyEvent, RequestContext

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


def test_apigw_proxy_event_contains_headers(apigw_proxy_event):
    evt = apigw_proxy_event
    assert evt.headers is not None
    headers = evt.headers
    assert all([hdr in headers for hdr in {"Via", "Cache-Control", "Accept"}])
    assert headers.get("Host") == "1234567890.execute-api.us-east-1.amazonaws.com"


def test_apigw_proxy_event_contains_querystrin_params(apigw_proxy_event):
    evt = apigw_proxy_event
    assert evt.query_string_parameters is not None
    qryparams = evt.query_string_parameters
    assert all([prm in qryparams for prm in {"foo", "foo2"}])
    assert qryparams.get("foo2") == "baz"


def test_apigw_proxy_event_contains_request_ctx(apigw_proxy_event):
    evt = apigw_proxy_event
    assert evt.request_context is not None
    ctx = evt.request_context
    assert isinstance(ctx, RequestContext)
    assert ctx.account_id == "123456789012"
    assert ctx.identity.user_agent == "Custom User Agent String"
