class AssociationAdminUser():
    """User class defining the users model"""
    
    def __init__(self ,associationId, governmentId ,status ,user_role ,email ,password ,country ,created_by,creation_date ,updated_by,updated_at):    
        
        self.associationId = associationId
        self.governmentId = governmentId
        self.status = status
        self.user_role = user_role
        self.email = email
        self.password=password
        self.country = country
        self.created_by = created_by
        self.creation_date = creation_date
        self.updated_by = updated_by
        self.updated_at = updated_at