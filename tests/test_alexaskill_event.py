import pytest

from aws_dataclasses.alexa_skill_event import AlexaSkillEvent

from .util import get_event_dict


@pytest.fixture(scope="module")
def alexa_event_raw():
    return get_event_dict("alexa-event.json")


@pytest.fixture(scope="module")
def alexa_event(alexa_event_raw):
    return AlexaSkillEvent.from_event(alexa_event_raw)


def test_alexa_skill(alexa_event):
    evt = alexa_event
    assert evt.event_version == "1.0"
    assert evt.request is not None
    assert evt.session is not None
    assert evt.context is not None


def test_skill_session(alexa_event):
    session = alexa_event.session
    assert session.application.applicationId == "amzn1.ask.skill.[unique-value-here]"
    assert session.session_id == "amzn1.echo-api.session.[unique-value-here]"
    assert session.new is False


def test_skill_request(alexa_event):
    request = alexa_event.request
    assert request.intent.name == "RecipeIntent"
    assert request.intent.slots.get("Item").value == "snowball"
    assert request.locale == "en-US"
