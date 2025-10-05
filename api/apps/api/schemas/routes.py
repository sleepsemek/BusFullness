from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class RouteAvgOut(BaseModel):
    asof: Optional[datetime] = Field(None, description="Самый свежий ts среди камер маршрута")
    occupancy_avg: Optional[float] = Field(
        None, ge=0, le=1,
        description="Средняя загрузка 0..1: среднее по автобусам, где каждый автобус усреднён по своим камерам"
    )
