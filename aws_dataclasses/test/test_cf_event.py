from unittest import TestCase

from aws_dataclasses.cf_event import CloudfrontEvent
from aws_dataclasses.http_proxy_event import ApiGwProxyEvent

from aws_dataclasses.test.util import get_event_dict


class TestProxyEvent(TestCase):
    def setUp(self):
        request_event_dict = get_event_dict("cf_request_event.json")
        response_event_dict = get_event_dict("cf_response_event.json")
        self.req_event = CloudfrontEvent.from_event(request_event_dict).first_record
        self.resp_event = CloudfrontEvent.from_event(response_event_dict).first_record

    def test_request(self):
        evt = self.req_event
        self.assertEqual(evt.config.request_id, "MRVMF7KydIvxMWfJIglgwHQwZsbG2IhRJ07sn9AkKUFSHS9EXAMPLE==")
        self.assertIsNone(evt.response)
        self.assertEqual(evt.request.querystring, "size=large")

    def test_response(self):
        evt = self.resp_event
        self.assertEqual(evt.config.request_id, "xGN7KWpVEmB9Dp7ctcVFQC4E-nrcOcEKS3QyAez--06dV7TEXAMPLE==")
        self.assertEqual(evt.response.status, "200")
        self.assertEqual(evt.request.client_ip, "2001:0db8:85a3:0:0:8a2e:0370:7334")
