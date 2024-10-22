from enum import Enum
from exceptions import *


class BrowserName(Enum):
    """
    Enum representing various web browser names.
    
    """
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
    """
    Represents a session with a title and description.
    
    Attributes:
        title (str): The title of the session.
        description (str): A description of the session.
        approved (bool): Indicates if the session is approved.
        
    """

    def __init__(self, title: str, description: str) -> None:
        """
        Initializes a new session with a title and description.

        Args:
            title (str): Title of the session.
            description (str): Description of the session.
            
        """
        self._approved: bool = False
        self._title: str = title
        self._description: str = description
        
    def getTitle(self) -> str:
        """
        Returns the title of the session.

        Returns:
            str: The title of the session.
            
        """
        return self._title

    def setTitle(self, title: str) -> None:
        """
        Sets the title of the session.

        Args:
            title (str): The new title of the session.
            
        """
        self._title = title

    def getDescription(self) -> str:
        """
        Returns the description of the session.

        Returns:
            str: The description of the session.
            
        """
        return self._description

    def setDescription(self, description: str) -> None:
        """
        Sets the description of the session.

        Args:
            description (str): The new description of the session.
            
        """
        self._description = description

    def isApproved(self) -> bool:
        """
        Returns whether the session is approved.

        Returns:
            bool: True if the session is approved, else False.
            
        """
        return self._approved
    
    def setApproved(self, approved: bool) -> None:
        """
        Sets the approval status of the session.

        Args:
            approved (bool): The new approval status.
            
        """
        self._approved = approved


class WebBrowser:
    """
    Represents a web browser and its major version.

    Attributes:
        name (BrowserName): The name of the browser.
        majorVersion (int): The major version of the browser.
        
    """

    def __init__(self, name: str, majorVersion: int) -> None:
        """
        Initializes a new web browser instance.

        Args:
            name (str): The name of the browser as a string.
            majorVersion (int): The major version of the browser.
            
        """
        self._name: BrowserName = self.TranslateStringToBrowserName(name)
        self._majorVersion: int = majorVersion

    def TranslateStringToBrowserName(self, name: str) -> BrowserName:
        """
        Translates a string representation of a browser name into the
        corresponding BrowserName Enum.

        Args:
            name (str): The name of the browser.

        Returns:
            BrowserName: The corresponding BrowserName Enum value.
            
        """
        if "IE" in name:
            return BrowserName.InternetExplorer
        # TODO: Add more logic for properly sniffing for other browsers.
        return BrowserName.Unknown

    def getName(self) -> BrowserName:
        """
        Returns the name of the browser.

        Returns:
            BrowserName: The name of the browser as an Enum.
            
        """
        return self._name

    def setName(self, name: BrowserName) -> None:
        """
        Sets the name of the browser.

        Args:
            name (BrowserName): The new browser name.
            
        """
        self._name = name
    
    def getMajorVersion(self) -> int:
        """
        Returns the major version of the browser.

        Returns:
            int: The major version of the browser.
            
        """
        return self._majorVersion

    def setMajorVersion(self, majorVersion: int) -> None:
        """
        Sets the major version of the browser.

        Args:
            majorVersion (int): The new major version.
            
        """
        self._majorVersion = majorVersion


class Speaker:
    """
    Represents a speaker with personal and professional details.

    Attributes:
        firstName (str): The speaker's first name.
        lastName (str): The speaker's last name.
        email (str): The speaker's email address.
        exp (int): The years of experience the speaker has.
        hasBlog (bool): Indicator of whether the speaker has a blog.
        blogURL (str): The URL of the speaker's blog, if applicable.
        browser (WebBrowser): The browser the speaker uses.
        certifications (list[str]): List of certifications held by the speaker.
        employer (str): The speaker's employer.
        registrationFee (int): The fee for the speaker's registration.
        sessions (list[Session]): List of sessions proposed by the speaker.
        
    """

    def __init__(self) -> None:
        """
        Initializes a new speaker instance with default values.
        
        """
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
        """
        Registers the speaker after validating requirements and 
        approvals and saves to the repository.

        Args:
            repository: The repository for saving the speaker.

        Returns:
            str: The ID of the registered speaker, or an empty string
            if registration fails.
            
        """
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
        """
        Validates the speaker’s required attributes before registration.

        Raises:
            ValueError: If any required field is empty.
            
        """
        if not self._firstName:
            raise ValueError("First Name is required.")
        if not self._lastName:
            raise ValueError("Last name is required.")
        if not self._email:
            raise ValueError("Email is required.")

    def meets_requirements(self) -> bool:
        """
        Checks if the speaker meets the registration requirements.

        Returns:
            bool: True if the speaker meets the criteria, else False.
            
        """
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
        """
        Checks and approves the speaker's sessions based on specific
        criteria.

        Returns:
            bool: True if at least one session is approved, else False.

        Raises:
            ValueError: If there are no sessions to approve.
            NoSessionsApprovedException: If no sessions are approved.
            
        """
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
        """
        Sets the registration fee based on the speaker's experience.

        Fee structure:
            0 for more than 10 years,
            50 for 6 to 9 years,
            100 for 4 to 5 years,
            250 for 2 to 3 years,
            500 for less than or equal to 1 year.
            
        """
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
        """
        Sets the first name of the speaker.

        Args:
            firstName (str): The first name of the speaker.
            
        """
        self._firstName = firstName
        
    def setLastName(self, lastName: str) -> None:
        """
        Sets the last name of the speaker.

        Args:
            lastName (str): The last name of the speaker.
            
        """
        self._lastName = lastName
    
    def setEmail(self, email: str) -> None:
        """
        Sets the email address of the speaker.

        Args:
            email (str): The email address of the speaker.
            
        """
        self._email = email
    
    def setEmployer(self, employer: str) -> None:
        """
        Sets the employer of the speaker.

        Args:
            employer (str): The name of the employer.
            
        """
        self._employer = employer
    
    def setHasBlog(self, hasBlog: bool) -> None:
        """
        Sets the blog ownership status of the speaker.

        Args:
            hasBlog (bool): True if the speaker has a blog, else False.
            
        """
        self._hasBlog = hasBlog
    
    def setBrowser(self, webBrowser: WebBrowser) -> None:
        """
        Sets the web browser used by the speaker.

        Args:
            webBrowser (WebBrowser): The speaker's browser instance.
            
        """
        self._browser = webBrowser
    
    def setExp(self, experience: int) -> None:
        """
        Sets the years of experience of the speaker.

        Args:
            experience (int): The years of experience.
            
        """
        self._exp = experience
    
    def setCertifications(self, certificates: list[str]) -> None:
        """
        Sets the certifications held by the speaker.

        Args:
            certificates (list[str]): List of certifications.
            
        """
        self._certifications = certificates
    
    def setBlogURL(self, blogURL: str) -> None:
        """
        Sets the URL of the speaker's blog.

        Args:
            blogURL (str): The URL of the blog.
            
        """
        self._blogURL = blogURL
        
    def setSessions(self, sessions: list[Session]) -> None:
        """
        Sets the list of sessions proposed by the speaker.

        Args:
            sessions (list[Session]): List of sessions for the speaker.
            
        """
        self._sessions = sessions