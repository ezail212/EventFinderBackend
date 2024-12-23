from pydantic import BaseModel

class User(BaseModel):
    Username: str
    Email: str
    Password: str