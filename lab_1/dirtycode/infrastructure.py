class Speaker:
    # Определите необходимые атрибуты и методы для класса Speaker
    def __init__(self, name: str):
        self.name = name

class IRepository:
    
    def saveSpeaker(self, speaker: Speaker) -> int:
        pass


class SqlServerRepository(IRepository):
    
    def saveSpeaker(self, speaker: Speaker) -> int:
        # TODO: Save speaker to SQL Server DB. For now, just assume success and return 1.
        return 1