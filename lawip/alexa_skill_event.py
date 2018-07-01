from collections import namedtuple
from typing import Dict

from lawip.log import get_logger

LOG = get_logger(__name__)

IntentSlot = namedtuple("IntentSlot", ['name', 'value'])
AlexaSkillUser = namedtuple("AlexaSkillUser", ["userId"])
AlexaSkillApplication = namedtuple("AlexaSkillApplication", ["applicationId"])


def parse_intents(slots: Dict[str, Dict[str, str]]) -> Dict[str, IntentSlot]:
    return {slot_name: IntentSlot(slot.get("key"),
                                  slot.get("value")) for slot_name, slot in slots.items()}


class AlexaIntent:
    def __init__(self, name: str,
                 **kwargs):
        self._name = name
        self._slots = parse_intents(kwargs.pop("slots")) if "slots" in kwargs else None
        if len(kwargs) > 0:
            LOG.warning(f"Got unexpected kwargs in {self.__class__} => {kwargs}")

    @classmethod
    def from_json(cls, intent: Dict):
        return cls(**intent)

    @property
    def name(self) -> str:
        return self._name

    @property
    def slots(self) -> Dict[str, IntentSlot]:
        return self._slots


class AlexaSkillRequest:
    def __init__(self, locale: str, timestamp: str,
                 type: str, requestId: str,
                 intent: Dict = None, reason: str = None,
                 **kwargs):
        self._locale = locale
        self._timestamp = timestamp
        self._request_id = requestId
        self._type = type
        self._intent = AlexaIntent(**intent) if isinstance(intent, dict) else None
        self._reason = reason
        if len(kwargs) > 0:
            LOG.warning(f"Unerwartete keyword-argumente gefunden in {self.__class__} => {kwargs}")

    @classmethod
    def from_json(cls, session: Dict):
        return cls(**session)

    @property
    def locale(self) -> str:
        return self._locale

    @property
    def timestamp(self) -> str:
        return self._timestamp

    @property
    def request_id(self) -> str:
        return self._request_id

    @property
    def type(self) -> str:
        return self._type

    @property
    def reason(self) -> str:
        return self._reason

    @property
    def intent(self) -> AlexaIntent:
        return self._intent


class AlexaSkillSession:
    def __init__(self, new: bool,
                 sessionId: str,
                 user: Dict[str, str],
                 application: Dict[str, str],
                 attributes: Dict = None,
                 **kwargs):
        self._new = new
        self._session_id = sessionId
        self._attributes = attributes
        self._user = AlexaSkillUser(**user)
        self._application = AlexaSkillApplication(**application)
        if len(kwargs) > 0:
            LOG.warning(f"Unerwartete keyword-argumente gefunden in {self.__class__} => {kwargs}")

    @classmethod
    def from_json(cls, session):
        return cls(**session)

    @property
    def new(self) -> bool:
        return self._new

    @property
    def session_id(self) -> str:
        return self._session_id

    @property
    def attributes(self) -> Dict:
        return self._attributes

    @property
    def user(self) -> AlexaSkillUser:
        return self._user

    @property
    def application(self) -> AlexaSkillApplication:
        return self._application


class AlexaSkillContext:
    def __init__(self, **kwargs):
        pass


class AlexaSkillEvent:
    def __init__(self, session: Dict,
                 version: str, request: Dict,
                 context: Dict, **kwargs):
        self._session = AlexaSkillSession(**session)
        self._version = version
        self._request = AlexaSkillRequest(**request)
        self._context = AlexaSkillContext(**context)
        if len(kwargs) > 0:
            LOG.warning(f"Unerwartete keyword-argumente gefunden in {self.__class__} => {kwargs}")

    @classmethod
    def from_event(cls, event):
        return cls(**event)

    @property
    def session(self) -> AlexaSkillSession:
        return self._session

    @property
    def event_version(self) -> str:
        return self._version

    @property
    def request(self) -> AlexaSkillRequest:
        return self._request

    @property
    def context(self) -> AlexaSkillContext:
        return self._context
