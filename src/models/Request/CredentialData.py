from pydantic import BaseModel

class CredentialData(BaseModel):
    Username: str
    Email: str
    Password: str