from collections import namedtuple
from typing import Dict

MessageAttribute = namedtuple("MessageAttribute", ['type', 'value'])


def parse_message_attributes(attrs):
    return {att_name: MessageAttribute(att.get("Type", None),
                                       att.get("Value", None)) for att_name, att in attrs.items()}


class Sns:
    def __init__(self, signature_version: str, timestamp: str, signature: str, signing_cert_url: str,
                 message_id: str, message: str, subject: str, message_attributes: Dict[str, MessageAttribute] = None,
                 type_: str = None, unsubscribe_url: str = None, topic_arn: str = None):
        self._signature_version = signature_version
        self._timestamp = timestamp
        self._signature = signature
        self._signing_cert_url = signing_cert_url
        self._message_id = message_id
        self._message = message
        self._subject = subject
        self._message_attributes = message_attributes
        self._type = type_
        self._unsubscribe_url = unsubscribe_url
        self._topic_arn = topic_arn

    @classmethod
    def from_json(cls, s3):
        message_attributes = parse_message_attributes(s3["MessageAttributes"])
        return cls(s3["SignatureVersion"],
                   s3["Timestamp"],
                   s3["Signature"],
                   s3["SigningCertUrl"],
                   s3["MessageId"],
                   s3["Message"],
                   s3["Subject"],
                   message_attributes,
                   s3["Type"],
                   s3["UnsubscribeUrl"],
                   s3["TopicArn"])

    @property
    def signature_version(self):
        return self._signature_version

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def signature(self):
        return self._signature

    @property
    def signing_cert_url(self):
        return self._signing_cert_url

    @property
    def message_id(self):
        return self._message_id

    @property
    def message(self):
        return self._message

    @property
    def subject(self):
        return self._subject

    @property
    def message_attributes(self):
        return self._message_attributes

    @property
    def type(self):
        return self._type

    @property
    def unsubscribe_url(self):
        return self._unsubscribe_url

    @property
    def topic_arn(self):
        return self._topic_arn


class SnsRecord:
    def __init__(self, event_version: str,
                 event_subscription_arn: str,
                 sns: Sns,
                 event_source: str):
        self._event_version = event_version
        self._event_source = event_source
        self._sns = sns
        self._event_subscription_arn = event_subscription_arn

    @classmethod
    def from_json(cls, record):
        return cls(record["EventVersion"],
                   record["EventSubscriptionArn"],
                   Sns.from_json(record["Sns"]),
                   record["EventSource"])

    @property
    def event_version(self):
        return self._event_version

    @property
    def sns(self):
        return self._sns

    @property
    def event_source(self):
        return self._event_source


class SnsEvent:
    def __init__(self, records: [SnsRecord]):
        self._records = records

    @classmethod
    def from_event(cls, event):
        return cls([SnsRecord.from_json(record) for record in event["Records"]])

    @property
    def records(self) -> [SnsRecord]:
        return self._records

    @property
    def first_record(self) -> SnsRecord:
        return self._records[0]
