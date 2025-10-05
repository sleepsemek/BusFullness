from pydantic import BaseModel
from datetime import datetime


class BusOut(BaseModel):
    id: int
    device_id: str
    route_id: str
    created_at: datetime
