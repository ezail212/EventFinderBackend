from pydantic import BaseModel

class LoggedinData(BaseModel):
    Username: str