class IRepository(object):
    
    def saveSpeaker(self, speaker):
        pass


class SqlServerRepository(IRepository):
    
    def saveSpeaker(self, speaker):
        # TODO: Save speaker to SQL Server DB. For now, just assume success and return 1.
        return 1