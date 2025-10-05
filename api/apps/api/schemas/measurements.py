from pydantic import BaseModel, Field
from datetime import datetime


class MeasurementIn(BaseModel):
    ts: datetime | None = None
    occupancy_pct: float = Field(..., ge=0.0, le=1.0)


class MeasurementOut(BaseModel):
    id: int
    camera_id: int
    ts: datetime
    occupancy_pct: float = Field(ge=0.0, le=1.0)
    created_at: datetime
