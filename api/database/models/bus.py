from datetime import datetime

import asyncpg
from dataclasses import dataclass


@dataclass
class Bus:
    id: int
    device_id: str
    route_id: str
    created_at: datetime

    @classmethod
    def from_record(cls, record: asyncpg.Record) -> "Bus":
        return cls(
            id=record["id"],
            device_id=record["device_id"],
            route_id=record["route_id"],
            created_at=record["created_at"],
        )
