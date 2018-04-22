from unittest2 import TestCase

from lawip.alexa_skill_event import AlexaSkillEvent
from lawip.sns_event import SnsEvent

from lawip.test.util import get_event_dict


class TestSnsEvent(TestCase):
    def setUp(self):
        event_dict = get_event_dict("alexa-event.json")
        self.event = AlexaSkillEvent.from_event(event_dict)

    def test_alexa_skill(self):
        evt = self.event
        self.assertEqual(evt.event_version, "1.0")
        self.assertIsNotNone(evt.request)
        self.assertIsNotNone(evt.session)
        self.assertIsNotNone(evt.context)

    def test_skill_session(self):
        session = self.event.session
        self.assertEqual(session.application.applicationId, "amzn1.ask.skill.[unique-value-here]")
        self.assertEqual(session.session_id, "amzn1.echo-api.session.[unique-value-here]")
        self.assertFalse(session.new)

    def test_skill_request(self):
        request = self.event.request
        self.assertEqual(request.intent.name, "RecipeIntent")
        self.assertEqual(request.intent.slots.get("Item").value, "snowball")
        self.assertEqual(request.locale, "en-US")
