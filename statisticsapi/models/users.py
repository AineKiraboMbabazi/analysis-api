class User():
    """User class defining the users model"""
    
    def __init__(self, associationId, name, status,email, password,country, user_group,user_role,created_by,creation_date):    
        self.associationId = associationId
        self.name = name
        self.status = status
        self.email = email
        self.password=password
        self.country = country
        self.user_group = user_group
        self.user_role = user_role
        self.created_by = created_by
        self.creation_date = creation_date
        