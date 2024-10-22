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
        speakerId: str = ""
        good: bool = False
        appr: bool = False
        ot: list[str] = ['Cobol', 'Punch Cards', 'Commodore', 'VBScript']
        
        domains: list[str] = ["aol.com", "hotmail.com", "prodigy.com", "compuserve.com"]
        
        if self._firstName:
            if self._lastName:                
                if self._email:
                    emps: list[str] = ["Pluralsight", "Microsoft", "Google", "Fog Creek Software", "37Signals", "Telerik"]
                    
                    good = (self._exp > 10 or self._hasBlog or len(self._certifications) > 3 or self._employer in emps)                    
                    if not good:
                        splitted: list[str] = self._email.split("@")
                        emailDomain: str = splitted[-1]

                        if not (emailDomain in domains) and not (self._browser.getName() == BrowserName.InternetExplorer and self._browser.getMajorVersion() < 9):
                            good = True
                    if good:
                        if len(self._sessions) != 0:
                            for session in self._sessions:
                                for tech in ot:
                                    if tech in session.getTitle() or tech in session.getDescription():
                                        session.setApproved(False)
                                        break
                                    else:
                                        session.setApproved(True)
                                        appr = True
                        else:
                            raise ValueError("Can't register speaker with no sessions to present.")                                                
                        if appr:
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
                            try:
                                speakerId = repository.saveSpeaker(self)
                            except Exception:
                                print("error") 
                            
                        else:
                            raise NoSessionsApprovedException("No sessions approved.")
                        
                    else:
                        raise SpeakerDoesntMeetRequirementsException("Speaker doesn't meet our arbitrary and capricious standards.")
                    
                else:
                    raise ValueError("Email is required.")
                                
            else:
                raise ValueError("Last name is required.")
                        
        else:
            raise ValueError("First Name is required")

        return speakerId
    
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