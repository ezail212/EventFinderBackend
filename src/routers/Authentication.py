from fastapi import APIRouter, Cookie
from fastapi.responses import JSONResponse
from starlette.requests import Request

from src.models.Request import LoggedInData
from src.models.Request.LoginData import LoginData
from src.common.AuthUtility import createAccessToken, decodeJWT
from typing import Union, Optional, Annotated

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"],
)

def getUser(data: LoginData):
    userDB = [{"Username": "superuser", "Password": "string", "Email": "superUser@gmail.com"}]

    for user in userDB:
        if data.Username.lower() == user["Username"].lower() or data.Email.lower() == user["Email"].lower():
            return user
    return None
@router.post("/login")
async def getLoginToken(data: LoginData):
    if not (data.Username and data.Email) or not data.Password:
        return JSONResponse({"msg": "Invalid Credentials"}, status_code=403)

    user = getUser(data)
    if not user:
        return JSONResponse({"msg": "User not found"}, status_code=404)

    accessToken = createAccessToken(user)
    if accessToken:
        response = JSONResponse({}, status_code=200)
        response.set_cookie(key="access_token", value=f'Bearer {accessToken}')
        return response

    return JSONResponse({"msg": "Unable to generate access token"}, status_code=401)

@router.post("/logout")
async def logout(request: Request):
    response = JSONResponse({"msg": "Logged out successfully"}, status_code=200)
    response.delete_cookie("access_token")
    return response

@router.post("/loggedIn")
async def checkLoggedIn(request: Request):
    data = await request.json()
    token = request.cookies.get("access_token")
    if not token or not data:
        return False

    decodedToken = decodeJWT(request.cookies.get("access_token").replace("Bearer ", ""))
    return data["Username"] == decodedToken["Username"]