from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from starlette.requests import Request

from src.models.Request.CredentialData import CredentialData
from src.common.AuthUtility import createAccessToken, decodeJWT
from src.common.DatabaseUtility import createUserEntry, checkUserExistsOrNot

security = HTTPBearer()
router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"]
)

def getUser(data: CredentialData):
    userDB = [{"Username": "superuser", "Password": "string", "Email": "superUser@gmail.com"}]

    for user in userDB:
        if (data.Username.lower() == user["Username"].lower() or data.Email.lower() == user["Email"].lower()) \
            and data.Password == user["Password"]:
            return user
    return None
@router.post("/login")
async def getLoginToken(data: CredentialData):
    if (not data.Username and not data.Email) or not data.Password:
        return JSONResponse({"msg": "Invalid Credentials"}, status_code=403)

    user = getUser(data)
    if not user:
        return JSONResponse({"msg": "User not found"}, status_code=404)

    accessToken = createAccessToken(user)
    if accessToken:
        response = JSONResponse(accessToken, status_code=200)
        response.set_cookie(key="access_token", value=f'Bearer {accessToken}')
        return response

    return JSONResponse({"msg": "Unable to generate access token"}, status_code=401)

@router.post("/logout")
async def logout(request: Request):
    response = JSONResponse({"msg": "Logged out successfully"}, status_code=200)
    response.delete_cookie("access_token")
    return response

@router.get("/getLoggedInUser")
async def getLoggedInUser(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        return ""

    decodedToken = decodeJWT(request.cookies.get("access_token").replace("Bearer ", ""))
    return decodedToken["Username"]

@router.post("/signUp")
async def signUp(loginData: CredentialData):
    if checkUserExistsOrNot(loginData):
        return JSONResponse({"msg": "User already exists!"}, status_code=400)

    createUserEntry(loginData)
    return JSONResponse({"msg": "User successfully signed up"}, status_code=200)