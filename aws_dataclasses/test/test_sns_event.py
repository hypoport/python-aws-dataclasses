from unittest import TestCase

from aws_dataclasses.sns_event import SnsEvent, SnsMessage

from aws_dataclasses.test.util import get_event_dict


class TestSnsEvent(TestCase):
    def setUp(self):
        self.event_dict = get_event_dict("sns-event.json")
        self.event = SnsEvent.from_event(self.event_dict).first_record

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

    def test_can_handle_missing_fields(self):
        sns = self.event_dict["Records"][0]["Sns"]
        sns.pop("MessageAttributes")
        res = SnsMessage(**sns)
        msg_attr = res.message_attributes
        self.assertIsNone(msg_attr)

    def test_can_handle_extra_fields(self):
        sns = self.event_dict["Records"][0]["Sns"]
        sns["TestAttr"] = 1234
        res = SnsMessage.from_json(sns)
