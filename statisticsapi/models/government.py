class Government():
    """Government class defining the Government model"""
    def __init__(self, userId, name, Location, status,created_by,creation_date):    
        self.userId = userId
        self.name = name
        self.Location = Location
        self.status = status
        self.created_by = created_by
        self.creation_date = creation_date
        