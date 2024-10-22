from enum import Enum
from exceptions import *


class BrowserName(Enum):
    Unknown = 1
    InternetExplorer = 2
    Firefox = 3
    Chrome = 4
    Opera = 5
    Safari = 6
    Dolphin = 7
    Konqueror = 8
    Linx = 9


class Session:
    def __init__(self, title: str, description: str) -> None:
        self._approved: bool = False
        self._title: str = title
        self._description: str = description
        
    def getTitle(self) -> str:
        return self._title

    def setTitle(self, title: str) -> None:
        self._title = title

    def getDescription(self) -> str:
        return self._description

    def setDescription(self, description: str) -> None:
        self._description = description

    def isApproved(self) -> bool:
        return self._approved
    
    def setApproved(self, approved: bool) -> None:
        self._approved = approved


class WebBrowser:
    def __init__(self, name: str, majorVersion: int) -> None:
        self._name: BrowserName = self.TranslateStringToBrowserName(name)
        self._majorVersion: int = majorVersion

    def TranslateStringToBrowserName(self, name: str) -> BrowserName:
        if "IE" in name:
            return BrowserName.InternetExplorer
        # TODO: Add more logic for properly sniffing for other browsers.
        return BrowserName.Unknown

    def getName(self) -> BrowserName:
        return self._name

    def setName(self, name: BrowserName) -> None:
        self._name = name
    
    def getMajorVersion(self) -> int:
        return self._majorVersion

    def setMajorVersion(self, majorVersion: int) -> None:
        self._majorVersion = majorVersion


class Speaker:
    def __init__(self) -> None:
        self._firstName: str = ""
        self._lastName: str = ""
        self._email: str = ""
        self._exp: int = 0
        self._hasBlog: bool = False
        self._blogURL: str = ""
        self._browser: WebBrowser = None
        self._certifications: list[str] = []
        self._employer: str = ""
        self._registrationFee: int = 0
        self._sessions: list[Session] = []

    def register(self, repository) -> str:
        self.validate_speaker()
        good = self.meets_requirements()
        appr = self.approve_sessions()

        if not good:
            raise SpeakerDoesntMeetRequirementsException(
                "Speaker doesn't meet our arbitrary and capricious standards."
            )

        self.set_registration_fee()

        try:
            speakerId = repository.saveSpeaker(self)
        except Exception:
            print("Error occurred while saving the speaker.")
            return ""

        return speakerId

    def validate_speaker(self) -> None:
        if not self._firstName:
            raise ValueError("First Name is required.")
        if not self._lastName:
            raise ValueError("Last name is required.")
        if not self._email:
            raise ValueError("Email is required.")

    def meets_requirements(self) -> bool:
        emp_list = [
            "Pluralsight", "Microsoft", "Google", 
            "Fog Creek Software", "37Signals", 
            "Telerik"
        ]
        domains = [
            "aol.com", "hotmail.com", "prodigy.com",
            "compuserve.com"
        ]

        good = (
            self._exp > 10 or self._hasBlog or
            len(self._certifications) > 3 or 
            self._employer in emp_list
        )

        if not good:
            emailDomain = self._email.split("@")[-1]
            if not (emailDomain in domains) and not (
                    self._browser.getName() == BrowserName.InternetExplorer and
                    self._browser.getMajorVersion() < 9
            ):
                good = True
                
        return good

    def approve_sessions(self) -> bool:
        ot = ['Cobol', 'Punch Cards', 'Commodore', 'VBScript']
        if len(self._sessions) == 0:
            raise ValueError("Can't register speaker with no sessions to present.")

        appr = False
        for session in self._sessions:
            approved = any(
                tech in session.getTitle() or 
                tech in session.getDescription() 
                for tech in ot
            )
            session.setApproved(not approved)
            appr = appr or not approved

        if not appr:
            raise NoSessionsApprovedException("No sessions approved.")

        return appr

    def set_registration_fee(self) -> None:
        if self._exp <= 1:
            self._registrationFee = 500
        elif 2 <= self._exp <= 3:
            self._registrationFee = 250
        elif 4 <= self._exp <= 5:
            self._registrationFee = 100
        elif 6 <= self._exp <= 9:
            self._registrationFee = 50
        else:
            self._registrationFee = 0
    
    def setFirstName(self, firstName: str) -> None:
        self._firstName = firstName
        
    def setLastName(self, lastName: str) -> None:
        self._lastName = lastName
    
    def setEmail(self, email: str) -> None:
        self._email = email
    
    def setEmployer(self, employer: str) -> None:
        self._employer = employer
    
    def setHasBlog(self, hasBlog: bool) -> None:
        self._hasBlog = hasBlog
    
    def setBrowser(self, webBrowser: WebBrowser) -> None:
        self._browser = webBrowser
    
    def setExp(self, experience: int) -> None:
        self._exp = experience
    
    def setCertifications(self, certificates: list[str]) -> None:
        self._certifications = certificates
    
    def setBlogURL(self, blogURL: str) -> None:
        self._blogURL = blogURL
        
    def setSessions(self, sessions: list[Session]) -> None:
        self._sessions = sessions