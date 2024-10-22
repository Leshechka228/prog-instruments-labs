import unittest
from domain import Speaker, WebBrowser, Session
from .infrastructure import SqlServerRepository
from exceptions import *


class Test(unittest.TestCase):

    def setUp(self) -> None:
        self._repository = SqlServerRepository()

    def tearDown(self) -> None:
        pass

    def getSpeakerThatWouldBeApproved(self) -> Speaker:
        speaker: Speaker = Speaker()
        speaker.setFirstName("First")
        speaker.setLastName("Last")
        speaker.setEmail("example@domain.com")
        speaker.setEmployer("Example Employer")
        speaker.setHasBlog(True)
        speaker.setBrowser(WebBrowser("test", 1))
        speaker.setExp(1)
        speaker.setBlogURL("")
        sessions: list[Session] = []
        sessions.append(Session("test title", "test description"))
        speaker.setSessions(sessions)

        return speaker
    
    def getSpeakerWithRedFlags(self) -> Speaker:
        speaker: Speaker = self.getSpeakerThatWouldBeApproved()
        speaker.setEmail("tom@aol.com")
        speaker.setBrowser(WebBrowser("IE", 6))
        return speaker

    def test_register_EmptyFirstName_RaisesValueError(self) -> None:
        speaker: Speaker = self.getSpeakerThatWouldBeApproved()
        speaker.setFirstName("")

        with self.assertRaises(ValueError):
            speaker.register(self._repository)

    def test_register_EmptyLastName_RaisesValueError(self) -> None:
        speaker: Speaker = self.getSpeakerThatWouldBeApproved()
        speaker.setLastName("")

        with self.assertRaises(ValueError):
            speaker.register(self._repository)

    def test_register_EmptyEmail_RaisesValueError(self) -> None:
        speaker: Speaker = self.getSpeakerThatWouldBeApproved()
        speaker.setEmail("")

        with self.assertRaises(ValueError):
            speaker.register(self._repository)

    def test_register_EmpWithRedFlags_ReturnsId(self) -> None:
        speaker: Speaker = self.getSpeakerWithRedFlags()
        speaker.setEmployer("Microsoft")

        speakerId: int = speaker.register(self._repository)
        self.assertTrue(speakerId)

    def test_register_BlogAndRedFlags_ReturnsId(self) -> None:
        speaker: Speaker = self.getSpeakerWithRedFlags()
        speakerId: int = speaker.register(self._repository)

        self.assertTrue(speakerId)

    def test_register_CertsAndRedFlags_ReturnsId(self) -> None:
        speaker: Speaker = self.getSpeakerWithRedFlags()
        speaker.setCertifications([
            "cert1", "cert2", "cert3", "cert4"
        ])

        speakerId: int = speaker.register(self._repository)
        self.assertTrue(speakerId)

    def test_register_OneOldTechSession_ThrowsNoSessionsApproved(self) -> None:
        speaker: Speaker = self.getSpeakerThatWouldBeApproved()
        speaker.setSessions([
            Session("Cobol for dummies", "Intro to Cobol")
        ])

        with self.assertRaises(NoSessionsApprovedException):
            speaker.register(self._repository)

    def test_register_NoSessions_ThrowsValueError(self) -> None:
        speaker: Speaker = self.getSpeakerThatWouldBeApproved()
        speaker.setSessions([])

        with self.assertRaises(ValueError):
            speaker.register(self._repository)

    def test_register_NoBlogOldBrowser_ThrowsException(self) -> None:
        speaker: Speaker = self.getSpeakerThatWouldBeApproved()
        speaker.setHasBlog(False)
        speaker.setBrowser(WebBrowser("IE", 6))

        with self.assertRaises(SpeakerDoesntMeetRequirementsException):
            speaker.register(self._repository)

    def test_register_NoBlogOldEmail_ThrowsException(self) -> None:
        speaker: Speaker = self.getSpeakerThatWouldBeApproved()
        speaker.setHasBlog(False)
        speaker.setEmail("name@aol.com")

        with self.assertRaises(SpeakerDoesntMeetRequirementsException):
            speaker.register(self._repository)