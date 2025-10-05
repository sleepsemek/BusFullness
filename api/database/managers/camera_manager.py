from typing import List

from database.async_db import AsyncDatabase
from database.models.camera import Camera


class CameraManager:
    def __init__(self, db: AsyncDatabase):
        self.db = db

    async def list_by_device_id(self, device_id: str) -> List[Camera]:
        sql = """
            SELECT c.id, c.bus_id, c.position, c.created_at
            FROM camera AS c
            JOIN bus AS b ON b.id = c.bus_id
            WHERE b.device_id = $1
            ORDER BY CASE c.position WHEN 'F' THEN 1 WHEN 'M' THEN 2 WHEN 'B' THEN 3 ELSE 4 END
        """
        rows = await self.db.fetch(sql, device_id)
        return [Camera.from_record(r) for r in rows]


