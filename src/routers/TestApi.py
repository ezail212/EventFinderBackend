from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBasic
from starlette import status

from src.common.AuthUtility import decodeJWT

security = HTTPBasic()

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Test"],
    dependencies=[Depends(security)]
)

@router.post("/test")
async def testApi(token: Annotated[str, Depends(security)]):
    if not token:
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Authorization token missing",
        headers={"Auth-Token": ""}
        )

    payload = decodeJWT(token)
    if payload:
        return payload["Email"]
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Authorization token not valid",
        headers={"Auth-Token": ""}
        )