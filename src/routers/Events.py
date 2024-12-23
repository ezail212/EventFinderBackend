from fastapi import APIRouter, HTTPException
from starlette.requests import Request
from src.models.Response.EventTypesResponse import EventTypesResponse
from src.common.Enums.EventTypeEnum import EventTypeEnum

router = APIRouter(
    prefix="/api/v1/events",
    tags=["Events"]
)

@router.get("/getEventTypes")
async def getEventTypes():
    try:
        return EventTypesResponse(
            EventTypes = [eventType for eventType in EventTypeEnum]
        )
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=str(e)
        )