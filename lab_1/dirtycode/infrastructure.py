class Speaker:
    """
    Class representing a speaker.

    Attributes:
        name (str): The name of the speaker.
        
    """

    def __init__(self, name: str):
        """
        Initializes a speaker with the given name.

        Args:
            name (str): The name of the speaker.
            
        """
        self.name = name


class IRepository:
    """
    Interface for speaker repositories.
    
    """

    def saveSpeaker(self, speaker: Speaker) -> int:
        """
        Saves a speaker to the repository.

        Args:
            speaker (Speaker): The speaker to be saved.

        Returns:
            int: The identifier of the saved speaker.
            
        """
        pass


class SqlServerRepository(IRepository):
    """
    Implementation of the IRepository interface for working with a 
    SQL Server database.
    
    """

    def saveSpeaker(self, speaker: Speaker) -> int:
        """
        Saves a speaker to the SQL Server database.

        For the current implementation, we assume successful saving and
        return 1.

        Args:
            speaker (Speaker): The speaker to be saved.

        Returns:
            int: The identifier of the saved speaker (always returning 1 
            in this case).
            
        """
        return 1