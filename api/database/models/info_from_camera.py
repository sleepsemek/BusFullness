from dataclasses import dataclass
from datetime import datetime

import asyncpg


@dataclass
class InfoFromCam:
    id: int
    camera_id: int
    ts: datetime
    occupancy_pct: int
    created_at: datetime

    @classmethod
    def from_record(cls, record: asyncpg.Record) -> "InfoFromCam":
        return cls(
            id=record["id"],
            camera_id=record["camera_id"],
            ts=record["ts"],
            occupancy_pct=record["occupancy_pct"],
            created_at=record["created_at"],
        )
