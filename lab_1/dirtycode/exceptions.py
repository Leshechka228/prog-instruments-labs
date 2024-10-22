class SpeakerDoesntMeetRequirementsException(Exception):
    """
    Exception raised when a speaker does not meet specific 
    requirements.
    
    Attributes:
        message (str): Explanation of the exception.
        
    """

    def __init__(self, message: str) -> None:
        """
        Initializes the exception with the provided message.
        
        Args:
            message (str): Explanation of why the exception occurred.
            
        """
        super().__init__(message)


class NoSessionsApprovedException(Exception):
    """
    Exception raised when there are no approved sessions available.
    
    Attributes:
        message (str): Explanation of the exception.
        
    """

    def __init__(self, message: str) -> None:
        """
        Initializes the exception with the provided message.

        Args:
            message (str): Explanation of why the exception occurred.
            
        """
        super().__init__(message)