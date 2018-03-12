from unittest2 import TestCase

from lawip.http_proxy_event import ApiGwProxyEvent

from lawip.test.util import get_event_dict


class TestProxyEvent(TestCase):
    def setUp(self):
        event_dict = get_event_dict("apigw-proxy-event.json")
        self.event = ApiGwProxyEvent.from_event(event_dict)

    def test_object(self):
        evt = self.event
        self.assertEqual(evt.path, "/path/to/resource")
        self.assertEqual(evt.http_method, "POST")
        self.assertEqual(evt.request_context.account_id, "123456789012")
