class UserDocument:
    def __init__(self, first_name: str, last_name: str, user_id: str = None):
        self.first_name = first_name
        self.last_name = last_name
        self.id = user_id or f"{first_name}_{last_name}"
    
    @classmethod
    def get_or_create(cls, first_name: str, last_name: str):
        print(f"Creating user: {first_name} {last_name}")
        return cls(first_name, last_name)
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def __str__(self):
        return f"UserDocument(id={self.id}, name={self.first_name} {self.last_name})"