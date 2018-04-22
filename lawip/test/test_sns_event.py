from unittest import TestCase

from lawip.sns_event import SnsEvent

from lawip.test.util import get_event_dict


class TestSnsEvent(TestCase):
    def setUp(self):
        event_dict = get_event_dict("sns-event.json")
        self.event = SnsEvent.from_event(event_dict).first_record

    def test_sns_record(self):
        evt = self.event
        self.assertEqual(evt.event_version, "1.0")
        self.assertEqual(evt.event_source, "aws:sns")

    def test_sns(self):
        sns = self.event.sns
        self.assertEqual(sns.message, "Hello from SNS!")
        self.assertEqual(sns.topic_arn, "arn:aws:sns:EXAMPLE")
        self.assertEqual(sns.signature, "EXAMPLE")

    def test_message_attributes(self):
        msg_attr = self.event.sns.message_attributes
        self.assertEqual(msg_attr.get("Test").value, "TestString")
        self.assertEqual(msg_attr.get("Test").type, "String")
