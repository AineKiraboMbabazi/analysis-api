class Government():
    """Government class defining the Government model"""
    def __init__(self, name, photo, status,  created_by, creation_date, updated_by, updated_at):    
        self.photo = photo
        self.name = name
        self.updated_by = updated_by
        self.status = status
        self.created_by = created_by
        self.creation_date = creation_date
        self.updated_at = updated_at