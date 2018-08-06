from unittest import TestCase

from aws_dataclasses.s3_event import S3Event
from .util import get_event_dict


class TestS3Event(TestCase):
    def setUp(self):
        event_dict = get_event_dict("s3-event.json")
        self.event = S3Event.from_event(event_dict)

    def test_object(self):
        evt = self.event
        self.assertEqual(evt.first_record.s3.object.key, "HappyFace.jpg")
        self.assertEqual(evt.first_record.s3.object.size, 1024)
        self.assertEqual(evt.first_record.s3.object.etag, "0123456789abcdef0123456789abcdef")
        self.assertEqual(evt.first_record.s3.object.sequencer, "0A1B2C3D4E5F678901")

    def test_bucket(self):
        evt = self.event
        self.assertEqual(evt.first_record.s3.bucket.name, "sourcebucket")
        self.assertEqual(evt.first_record.s3.bucket.arn, "arn:aws:s3:::mybucket")

    def test_s3(self):
        evt = self.event
        self.assertEqual(evt.first_record.s3.configuration_id, "testConfigRule")
        self.assertEqual(evt.first_record.s3.s3_schemaversion, "1.0")

    def test_record(self):
        evt = self.event
        self.assertEqual(evt.first_record.event_time.strftime('%Y-%m-%dT%H:%M:%S%z'), "1970-01-01T00:00:00+0000")
        self.assertEqual(evt.first_record.event_version, "2.0")
        self.assertEqual(evt.first_record.aws_region, "us-east-1")
        self.assertEqual(evt.first_record.event_name, "ObjectCreated:Put")
