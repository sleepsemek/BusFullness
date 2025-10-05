from dataclasses import dataclass
from datetime import datetime

import asyncpg


@dataclass
class Camera:
    id: int
    bus_id: int
    position: str
    created_at: datetime

    @classmethod
    def from_record(cls, record: asyncpg.Record) -> "Camera":
        return cls(
            id=record["id"],
            bus_id=record["bus_id"],
            position=record["position"],
            created_at=record["created_at"],
        )
