class User():
    """User class defining the users model"""
    
    def __init__(self, first_name ,last_name ,other_name ,photo ,associationId ,governmentId ,status ,user_role ,email ,password ,country ,created_by,creation_date ,updated_by,updated_at):    
        
        self.first_name = first_name
        self.last_name = last_name
        self.other_name = other_name
        self.photo = photo
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