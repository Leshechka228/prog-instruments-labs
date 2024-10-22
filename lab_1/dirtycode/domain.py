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


class Session(object):

    def __init__(self, title, description):
        '''
        Constructor
        '''
        self._approved = False
        self._title = title
        self._description = description
        
    def getTitle(self):
        return self._title

    def setTitle(self, title):
        self._title = title

    def getDescription(self):
        return self._description

    def setDescription(self, description):
        self._description = description

    def isApproved(self):
        return self._approved
    
    def setApproved(self, approved):
        self._approved = approved


class WebBrowser(object):
    
    def __init__(self, name, majorVersion):
        self._name = self.TranslateStringToBrowserName(name)
        self._majorVersion = majorVersion

    def TranslateStringToBrowserName(self, name):
        if "IE" in name:
            return BrowserName.InternetExplorer
        # TODO: Add more logic for properly sniffing for other browsers.
        return BrowserName.Unknown

    def getName(self):
        return self._name

    def setName(self, name):
        self._name = name
    
    def getMajorVersion(self):
        return self._majorVersion

    def setMajorVersion(self, majorVersion):
        self._majorVersion = majorVersion


class Speaker(object):

    def __init__(self):
        self._firstName = ""
        self._lastName = ""
        self._email = ""
        self._exp = 0
        self._hasBlog = False
        self._blogURL = ""
        self._browser = None
        self._certifications = []
        self._employer = ""
        self._registrationFee = 0
        self._sessions = []

    def register(self, repository):
        speakerId = ""
        good = False
        appr = False
        #nt = [ "Microservices", "Node.js", "CouchDB", "KendoUI", "Dapper", "Angular2" ]
        ot = ['Cobol', 'Punch Cards', 'Commodore', 'VBScript']
        
        #DEFECT #5274 DA 12/10/2012
        #We weren't filtering out the prodigy domain so I added it.
        domains = ["aol.com", "hotmail.com", "prodigy.com", "compuserve.com"]
        
        if (self._firstName):            
            if (self._lastName):                
                if (self._email):
                    #put list of employers in array
                    emps = ["Pluralsight", "Microsoft", "Google", "Fog Creek Software", "37Signals", "Telerik"]
                    
                    #DFCT #838 Jimmy
                    #We're now requiring 3 certifications so I changed the hard coded number. Boy, programming is hard.
                    good = ((self._exp > 10 or self._hasBlog or len(self._certifications) > 3 or self._employer in emps))                    
                    if (not good):
                        #need to get just the domain from the email
                        splitted = self._email.split("@")
                        emailDomain = splitted[len(splitted) - 1]

                        if (not (emailDomain in domains) and (not(self._browser.getName() == BrowserName.InternetExplorer and self._browser.getMajorVersion() < 9))):
                            good = True
                    if (good):
                        #DEFECT #5013 CO 1/12/2012
                        #We weren't requiring at least one session
                        if (len(self._sessions) != 0):
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
                        if (appr):
                            #if we got this far, the speaker is approved
                            #let's go ahead and register him/her now.
                            #First, let's calculate the registration fee.
                            #More experienced speakers pay a lower fee.
                            if (self._exp <= 1):
                                self._registrationFee = 500
                            
                            elif (self._exp >= 2 and self._exp <= 3):
                                self._registrationFee = 250
                            
                            elif (self._exp >= 4 and self._exp <= 5):
                                self._registrationFee = 100
                            
                            elif (self._exp >= 6 and self._exp <= 9):
                                self._registrationFee = 50
                            
                            else:
                                self._registrationFee = 0                                                        
                            #Now, save the speaker and sessions to the db.
                            try:
                                speakerId = repository.saveSpeaker(self)
                            except Exception:
                                #in case the db call fails
                                print("error") 
                            
                        else:
                            raise NoSessionsApprovedException("No sessions approved.")
                        
                    else:
                        raise SpeakerDoesntMeetRequirementsException("Speaker doesn't meet our abitrary and capricious standards.")
                    
                else:
                    raise ValueError("Email is required.")
                                
            else:
                raise ValueError("Last name is required.")
                        
        else:
            raise ValueError("First Name is required")


        return speakerId
    
    def setFirstName(self, firstName):
        self._firstName = firstName
        
    def setLastName(self, lastName):
        self._lastName = lastName
    
    def setEmail(self, email):
        self._email = email
    
    def setEmployer(self, employer):
        self._employer = employer
    
    def setHasBlog(self, hasBlog):
        self._hasBlog = hasBlog
    
    def setBrowser(self, webBrowser):
        self._browser = webBrowser
    
    def setExp(self, experience):
        self._experience = experience
    
    def setCertifications(self, certificates):
        self._certifications = certificates
    
    def setBlogURL(self, blogURL):
        self._blogURL = blogURL
        
    def setSessions(self, sessions):
        self._sessions = sessions
