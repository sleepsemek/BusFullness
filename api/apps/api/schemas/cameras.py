from pydantic import BaseModel
from datetime import datetime


class CameraOut(BaseModel):
    id: int
    bus_id: int
    position: str
    created_at: datetime
