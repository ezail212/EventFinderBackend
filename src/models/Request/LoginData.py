from pydantic import BaseModel

class LoginData(BaseModel):
    Username: str
    Email: str
    Password: str