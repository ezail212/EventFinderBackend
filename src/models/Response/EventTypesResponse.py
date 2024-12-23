from pydantic import BaseModel
from typing import List
from src.common.Enums.EventTypeEnum import EventTypeEnum

class EventTypesResponse(BaseModel):
    EventTypes: List[EventTypeEnum]