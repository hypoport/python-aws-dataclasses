import json
from collections import namedtuple
from typing import Dict, List

from dataclasses import dataclass, field, InitVar

from aws_dataclasses.util import handle_nonexisting_fields

MessageAttribute = namedtuple("MessageAttribute", ['type', 'value'])


def parse_message_attributes(attrs):
    return {att_name: MessageAttribute(att.get("Type", None),
                                       att.get("Value", None)) for att_name, att in attrs.items()}


@dataclass
class SnsMessage:
    signature_version: str = field(init=False)
    timestamp: str = field(init=False)
    signature: str = field(init=False)
    subject: str = field(init=False)
    message_id: str = field(init=False)
    message: str = field(init=False)
    type: str = field(init=False)
    topic_arn: str = field(init=False)
    signing_cert_url: str = field(init=False, default=None)
    unsubscribe_url: str = field(init=False, default=None)
    message_attributes: Dict = field(init=False, default=None)
    SignatureVersion: InitVar[str] = field(repr=False)
    Timestamp: InitVar[str] = field(repr=False)
    Signature: InitVar[str] = field(repr=False)
    SigningCertUrl: InitVar[str] = field(repr=False)
    MessageId: InitVar[str] = field(repr=False)
    Message: InitVar[str] = field(repr=False)
    Subject: InitVar[str] = field(repr=False)
    Type: InitVar[str] = field(repr=False)
    UnsubscribeUrl: InitVar[str] = field(repr=False)
    TopicArn: InitVar[str] = field(repr=False)
    MessageAttributes: InitVar[Dict] = field(repr=False, default=None)

    def __post_init__(self, SignatureVersion: str, Timestamp: str, Signature: str, SigningCertUrl: str, MessageId: str,
                      Message: str, Subject: str, Type: str, UnsubscribeUrl: str,
                      TopicArn: str, MessageAttributes: Dict):
        self.signature_version = SignatureVersion
        self.signature = Signature
        self.topic_arn = TopicArn
        self.type = Type
        self.unsubscribe_url = UnsubscribeUrl
        self.timestamp = Timestamp
        self.message = Message
        self.message_id = MessageId
        self.subject = Subject
        self.signing_cert_url = SigningCertUrl
        if MessageAttributes is not None:
            self.message_attributes = parse_message_attributes(MessageAttributes)

    @classmethod
    def from_json(cls, sns):
        if isinstance(sns, str):
            sns = json.loads(sns)
        sns = handle_nonexisting_fields(sns, cls)
        return cls(**sns)


@dataclass
class SnsRecord:
    event_source: str = field(init=False)
    sns: SnsMessage = field(init=False)
    event_version: str = field(init=False)
    event_subscription_arn: str = field(init=False)
    EventVersion: InitVar[str] = field(repr=False)
    EventSubscriptionArn: InitVar[str] = field(repr=False)
    Sns: InitVar[Dict] = field(repr=False)
    EventSource: InitVar[str] = field(repr=False)

    def __post_init__(self, EventVersion: str, EventSubscriptionArn: str, Sns: Dict, EventSource: str):
        self.event_source = EventSource
        self.event_version = EventVersion
        self.event_subscription_arn = EventSubscriptionArn
        self.sns = SnsMessage(**Sns)

    @classmethod
    def from_json(cls, record):
        if isinstance(record, str):
            record = json.loads(record)
        record = handle_nonexisting_fields(record, cls)
        return cls(**record)


@dataclass
class SnsEvent:
    records: List[SnsRecord] = field(init=False)
    first_record: SnsRecord = field(init=False)
    Records: InitVar[List] = field(repr=False)

    def __post_init__(self, Records: List):
        self.records = [SnsRecord(**record) for record in Records]
        self.first_record = self.records[0]

    @classmethod
    def from_event(cls, event):
        if isinstance(event, str):
            event = json.loads(event)
        event = handle_nonexisting_fields(event, cls)
        return cls(**event)
