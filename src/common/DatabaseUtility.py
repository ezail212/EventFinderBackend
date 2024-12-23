from src.models.Request.CredentialData import CredentialData
from src.models.Database.User import User

def checkUserExistsOrNot(loginData: CredentialData):
    db = [{"Username": "superuser", "Email": "", "Password": "string"}]

    for data in db:
        if loginData.Username == data["Username"] or loginData.Email == data["Email"]:
            return True

    return False

def createUserEntry(loginData: CredentialData):
    pass