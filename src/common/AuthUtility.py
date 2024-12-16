from datetime import datetime, timedelta
import jwt
from src.Config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM, REFRESH_TOKEN_EXPIRE_TIME_MINUTES, REFRESH_SECRET_KEY
from typing import Union, Any, Optional
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import HTTPException, Request

async def checkCookie(request: Request):
    cookie = request.cookies
    if not cookie:
        return None
    if cookie.get('refresh-Token'):
        return cookie.get('refresh-Token')

def createAccessToken(data: dict, expiryTime: timedelta = None):
  dataToEncode = {"Username": data["Username"], "Email": data["Email"]}
  if expiryTime:
    expire = datetime.utcnow() + expiryTime
  else:
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  dataToEncode.update({"exp": expire})
  encodedJwt = jwt.encode(dataToEncode, SECRET_KEY, algorithm=ALGORITHM)
  return encodedJwt

def createRefreshToken(subject: dict, expiresDelta: timedelta = None) -> str:
    if expiresDelta:
      expiresDelta = datetime.utcnow() + expiresDelta
    else:
      expiresDelta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_TIME_MINUTES)

    dataToEncode = {"exp": expiresDelta, "sub": subject}
    encodedJwt = jwt.encode(dataToEncode, REFRESH_SECRET_KEY, ALGORITHM)
    return encodedJwt

def decodeJWT(jwToken: str):
    try:
        payload = jwt.decode(jwToken, SECRET_KEY, ALGORITHM)
        return payload
    except:
        return

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            token = credentials.credentials
            if not self.verifyJwt(token):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return token
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verifyJwt(self, jwtoken: str) -> bool:
        try:
            decodeJWT(jwtoken)
            return True
        except jwt.ExpiredSignatureError:
            return False
        except jwt.PyJWTError:
            return False