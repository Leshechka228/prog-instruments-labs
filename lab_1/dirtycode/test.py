import unittest
from domain import Speaker, WebBrowser, Session
from .infrastructure import SqlServerRepository
from exceptions import *


class Test(unittest.TestCase):

    def setUp(self) -> None:
        """
        Sets up the test environment by initializing the repository.

        This method runs before each test method to prepare the necessary
        components for the tests.
        
        """
        self._repository = SqlServerRepository()

    def tearDown(self) -> None:
        """
        Cleans up after each test method.

        This method runs after each test method, allowing for any necessary
        cleanup tasks.
        
        """
        pass

    def getSpeakerThatWouldBeApproved(self) -> Speaker:
        """
        Creates and returns a Speaker instance that meets approval criteria.

        Returns:
            Speaker: An approved speaker with valid attributes.
            
        """
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
        """
        Creates a Speaker instance with attributes that raise red flags.

        Returns:
            Speaker: A speaker with specified red flag attributes.
            
        """
        speaker: Speaker = self.getSpeakerThatWouldBeApproved()
        speaker.setEmail("tom@aol.com")
        speaker.setBrowser(WebBrowser("IE", 6))
        return speaker

    def test_register_EmptyFirstName_RaisesValueError(self) -> None:
        """
        Tests that registering a speaker with an empty first name
        raises a ValueError.
        
        """
        speaker: Speaker = self.getSpeakerThatWouldBeApproved()
        speaker.setFirstName("")

        with self.assertRaises(ValueError):
            speaker.register(self._repository)

    def test_register_EmptyLastName_RaisesValueError(self) -> None:
        """
        Tests that registering a speaker with an empty last name
        raises a ValueError.
        
        """
        speaker: Speaker = self.getSpeakerThatWouldBeApproved()
        speaker.setLastName("")

        with self.assertRaises(ValueError):
            speaker.register(self._repository)

    def test_register_EmptyEmail_RaisesValueError(self) -> None:
        """
        Tests that registering a speaker with an empty email
        raises a ValueError.
        
        """
        speaker: Speaker = self.getSpeakerThatWouldBeApproved()
        speaker.setEmail("")

        with self.assertRaises(ValueError):
            speaker.register(self._repository)

    def test_register_EmpWithRedFlags_ReturnsId(self) -> None:
        """
        Tests that registering a speaker with red flags but valid
        employer returns an ID.
        
        """
        speaker: Speaker = self.getSpeakerWithRedFlags()
        speaker.setEmployer("Microsoft")

        speakerId: int = speaker.register(self._repository)
        self.assertTrue(speakerId)

    def test_register_BlogAndRedFlags_ReturnsId(self) -> None:
        """
        Tests that registering a speaker with a blog and red flags
        returns an ID.
        
        """
        speaker: Speaker = self.getSpeakerWithRedFlags()
        speakerId: int = speaker.register(self._repository)

        self.assertTrue(speakerId)

    def test_register_CertsAndRedFlags_ReturnsId(self) -> None:
        """
        Tests that registering a speaker with certifications and red flags
        returns an ID.
        
        """
        speaker: Speaker = self.getSpeakerWithRedFlags()
        speaker.setCertifications([
            "cert1", "cert2", "cert3", "cert4"
        ])

        speakerId: int = speaker.register(self._repository)
        self.assertTrue(speakerId)

    def test_register_OneOldTechSession_ThrowsNoSessionsApproved(self) -> None:
        """
        Tests that registering a speaker with an outdated tech session
        raises a NoSessionsApprovedException.
        
        """
        speaker: Speaker = self.getSpeakerThatWouldBeApproved()
        speaker.setSessions([
            Session("Cobol for dummies", "Intro to Cobol")
        ])

        with self.assertRaises(NoSessionsApprovedException):
            speaker.register(self._repository)

    def test_register_NoSessions_ThrowsValueError(self) -> None:
        """
        Tests that registering a speaker with no sessions raises
        a ValueError.
        
        """
        speaker: Speaker = self.getSpeakerThatWouldBeApproved()
        speaker.setSessions([])

        with self.assertRaises(ValueError):
            speaker.register(self._repository)

    def test_register_NoBlogOldBrowser_ThrowsException(self) -> None:
        """
        Tests that registering a speaker with no blog and an old browser
        raises a SpeakerDoesntMeetRequirementsException.
        
        """
        speaker: Speaker = self.getSpeakerThatWouldBeApproved()
        speaker.setHasBlog(False)
        speaker.setBrowser(WebBrowser("IE", 6))

        with self.assertRaises(SpeakerDoesntMeetRequirementsException):
            speaker.register(self._repository)

    def test_register_NoBlogOldEmail_ThrowsException(self) -> None:
        """
        Tests that registering a speaker with no blog and an old email
        raises a SpeakerDoesntMeetRequirementsException.
        
        """
        speaker: Speaker = self.getSpeakerThatWouldBeApproved()
        speaker.setHasBlog(False)
        speaker.setEmail("name@aol.com")

        with self.assertRaises(SpeakerDoesntMeetRequirementsException):
            speaker.register(self._repository)