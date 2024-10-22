import unittest
from domain import Speaker, WebBrowser, Session
from .infrastructure import SqlServerRepository
from exceptions import *


class Test(unittest.TestCase):
    
    def setUp(self):        
        self._repository = SqlServerRepository()
        
        pass

    def tearDown(self):
        pass

    def test_register_EmptyFirstName_ThrowsArgumentNullException(self):
        speaker = self.getSpeakerThatWouldBeApproved()
        speaker.setFirstName("")
        
        with self.assertRaises(ValueError):
            speaker.register(self._repository)
            
    def test_register_EmptyLastName_ThrowsArgumentNullException(self):
        speaker = self.getSpeakerThatWouldBeApproved()
        speaker.setLastName("")
        
        with self.assertRaises(ValueError):
            speaker.register(self._repository)
    
    def test_register_EmptyEmail_ThrowsArgumentNullException(self):
        speaker = self.getSpeakerThatWouldBeApproved()
        speaker.setEmail("")
    
        with self.assertRaises(ValueError):
            speaker.register(self._repository)
    
    def test_register_WorksForPrestigiousEmployerButHasRedFlags_ReturnsSpeakerId(self):
        speaker = self.getSpeakerWithRedFlags()
        speaker.setEmployer("Microsoft")

        # act
        speakerId = speaker.register(SqlServerRepository())

        # assert
        self.assertTrue(speakerId)
        
    def test_register_HasBlogButHasRedFlags_ReturnsSpeakerId(self):
        speaker = self.getSpeakerWithRedFlags()

        speakerId = speaker.register(SqlServerRepository())

        self.assertTrue(speakerId)
    
    def test_register_HasCertificationsButHasRedFlags_ReturnsSpeakerId(self):
        speaker = self.getSpeakerWithRedFlags()
        speaker.setCertifications(["cert1", "cert2", "cert3", "cert4"])

        speakerId = speaker.register(SqlServerRepository())

        self.assertTrue(speakerId)
    
    
    def test_register_SingleSessionThatsOnOldTech_ThrowsNoSessionsApprovedException(self):
        speaker = self.getSpeakerThatWouldBeApproved()
        speaker.setSessions([Session("Cobol for dummies", "Intro to Cobol")])
        
        with self.assertRaises(NoSessionsApprovedException):
            speaker.register(SqlServerRepository())
        

    def test_register_NoSessionsPassed_ThrowsArgumentException(self):
        speaker = self.getSpeakerThatWouldBeApproved()
        speaker.setSessions([])
        
        with self.assertRaises(ValueError):
            speaker.register(self._repository)
    
    def test_register_DoesntAppearExceptionalAndUsingOldBrowser_ThrowsNoSessionsApprovedException(self):
        speakerThatDoesntAppearExceptional = self.getSpeakerThatWouldBeApproved()
        speakerThatDoesntAppearExceptional.setHasBlog(False)
        speakerThatDoesntAppearExceptional.setBrowser(WebBrowser("IE", 6))
        
        with self.assertRaises(SpeakerDoesntMeetRequirementsException):
            speakerThatDoesntAppearExceptional.register(self._repository)
    
    
    def test_register_DoesntAppearExceptionalAndHasAncientEmail_ThrowsNoSessionsApprovedException(self):
        speakerThatDoesntAppearExceptional = self.getSpeakerThatWouldBeApproved()
        speakerThatDoesntAppearExceptional.setHasBlog(False)
        speakerThatDoesntAppearExceptional.setEmail("name@aol.com")
        
        with self.assertRaises(SpeakerDoesntMeetRequirementsException):
            speakerThatDoesntAppearExceptional.register(self._repository)
               
    def getSpeakerThatWouldBeApproved(self):
        speaker = Speaker ()

        speaker.setFirstName("First")
        speaker.setLastName("Last")
        speaker.setEmail("example@domain.com")
        speaker.setEmployer("Example Employer")
        speaker.setHasBlog(True)
        speaker.setBrowser(WebBrowser ("test", 1))
        speaker.setExp(1)
        speaker.setBlogURL("")
        sessions = []
        sessions.append(Session("test title", "test description"))
        speaker.setSessions(sessions)

        return speaker
    
    def getSpeakerWithRedFlags(self):
        speaker = self.getSpeakerThatWouldBeApproved()
        speaker.setEmail("tom@aol.com")
        speaker.setBrowser(WebBrowser("IE", 6))
        return speaker
    
    
if __name__ == "__main__":

    unittest.main()