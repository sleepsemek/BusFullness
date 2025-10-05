from pydantic import BaseModel, RootModel
from datetime import datetime
from typing import Dict, List


class BusSnapshot(BaseModel):
    ts: datetime | None
    values: List[float]


class BusSnapshots(RootModel[Dict[str, BusSnapshot]]):
    pass
