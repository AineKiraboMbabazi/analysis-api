class Association():
    """Association class defining the association model"""
    def __init__(self, name, photo, status, governmentId, created_by, creation_date, updated_by, updated_at):    
        self.photo = photo
        self.name = name
        self.governmentId = governmentId
        self.updated_by = updated_by
        self.updated_at = updated_at
        self.status = status
        self.created_by = created_by
        self.creation_date = creation_date
        