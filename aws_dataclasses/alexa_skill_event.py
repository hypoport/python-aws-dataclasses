from collections import namedtuple
from datetime import datetime
from typing import Dict

import arrow
from dataclasses import dataclass, InitVar, field

from aws_dataclasses.base import GenericDataClass, EventClass

IntentSlot = namedtuple("IntentSlot", ['name', 'value'])
AlexaSkillUser = namedtuple("AlexaSkillUser", ["userId"])
AlexaSkillApplication = namedtuple("AlexaSkillApplication", ["applicationId"])


def _parse_intents(slots: Dict[str, Dict[str, str]]) -> Dict[str, IntentSlot]:
    return {slot_name: IntentSlot(slot.get("name"),
                                  slot.get("value")) for slot_name, slot in slots.items()}


@dataclass
class AlexaIntent(GenericDataClass):
    name: str
    slots: Dict[str, IntentSlot]

    def __post_init__(self):
        self.slots = _parse_intents(self.slots) if self.slots is not None else self.slots


@dataclass
class AlexaSkillRequest(GenericDataClass):
    locale: str
    timestamp: datetime
    request_id: str = field(init=False)
    type: str
    reason: str = field(default=None)
    should_link_result_be_returned: bool = field(init=False)
    intent: AlexaIntent = field(default=None)
    requestId: InitVar[str] = field(repr=False, default=None)
    shouldLinkResultBeReturned: InitVar[bool] = field(repr=False, default=None)

    def __post_init__(self, requestId: str, shouldLinkResultBeReturned: bool):
        self.timestamp = arrow.get(self.timestamp).datetime
        self.request_id = requestId
        self.should_link_result_be_returned = shouldLinkResultBeReturned
        self.intent = AlexaIntent.from_json(self.intent) if self.intent is not None else self.intent


@dataclass
class AlexaSkillSession(GenericDataClass):
    new: bool
    session_id: str = field(init=False)
    user: AlexaSkillUser
    application: AlexaSkillApplication
    attributes: Dict = field(default=None)
    sessionId: InitVar[str] = field(repr=False, default=None)

    def __post_init__(self, sessionId: str):
        self.session_id = sessionId
        self.user = AlexaSkillUser(**self.user)
        self.application = AlexaSkillApplication(**self.application)


@dataclass
class AlexaSkillContext(GenericDataClass):
    pass


@dataclass
class AlexaSkillEvent(EventClass):
    session: AlexaSkillSession
    version: str
    request: AlexaSkillRequest
    context: AlexaSkillContext

    def __post_init__(self):
        self.session = AlexaSkillSession.from_json(self.session)
        self.request = AlexaSkillRequest.from_json(self.request)
        self.context = AlexaSkillContext.from_json(self.context)
