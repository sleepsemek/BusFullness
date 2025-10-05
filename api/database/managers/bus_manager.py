from typing import List

from database.async_db import AsyncDatabase
from database.models.bus import Bus


class BusManager:
    def __init__(self, db: AsyncDatabase):
        self.db = db

    async def list_buses(self) -> List[Bus]:
        sql = """
              SELECT id, device_id, route_id, created_at
              FROM bus
              ORDER BY id
              """
        rows = await self.db.fetch(sql)
        return [Bus.from_record(r) for r in rows]
