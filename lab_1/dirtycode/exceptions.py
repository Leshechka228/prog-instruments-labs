class SpeakerDoesntMeetRequirementsException(Exception):
    
    def __init__(self, message: str) -> None:
        super().__init__(message)


class NoSessionsApprovedException(Exception):
    
    def __init__(self, message: str) -> None:
        super().__init__(message)