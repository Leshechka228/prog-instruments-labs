class SpeakerDoesntMeetRequirementsException(Exception):
    
    def __init__(self, message):

        super().__init__(message)

        
class NoSessionsApprovedException(Exception):
    
    def __init__(self, message):

        super().__init__(message)