from collections import defaultdict
from datetime import datetime, timezone
from typing import Optional, List

import asyncpg

from database.async_db import AsyncDatabase


class InfoFromCameraManager:
    def __init__(self, db: AsyncDatabase):
        self.db = db

    async def fetch_snapshot_by_device_ids(self, device_ids: list[str]) -> list[dict]:
        """
        Возвращает строки: device_id, camera_id, position, ts, occupancy_pct
        """
        sql = """
              WITH last_per_cam AS (SELECT DISTINCT ON (i.camera_id) i.camera_id,
                                                                     i.ts,
                                                                     i.occupancy_pct
                                    FROM info_from_camera i
                                    ORDER BY i.camera_id, i.ts DESC)
              SELECT b.device_id,
                     c.id       AS camera_id,
                     c.position AS position,
                     l.ts       AS ts,
                     l.occupancy_pct
              FROM bus b
                       JOIN camera c ON c.bus_id = b.id
                       LEFT JOIN last_per_cam l ON l.camera_id = c.id
              WHERE b.device_id = ANY ($1::text[])
              ORDER BY b.device_id,
                       CASE c.position WHEN 'F' THEN 1 WHEN 'M' THEN 2 WHEN 'B' THEN 3 ELSE 4 END;
              """
        rows = await self.db.fetch(sql, device_ids)
        return [dict(r) for r in rows]

    async def fetch_route_avg(self, route_id: str) -> Optional[dict]:
        """
        Возвращает среднюю загрузку маршрута и последний ts
        """
        # Все device_id автобусов маршрута
        rows_bus = await self.db.fetch("SELECT device_id FROM bus WHERE route_id = $1", route_id)
        device_ids = [r["device_id"] for r in rows_bus]
        if not device_ids:
            return None

        # Последние измерения по всем камерам этих автобусов
        rows = await self.fetch_snapshot_by_device_ids(device_ids)
        if not rows:
            return None

        # Агрегация
        last_ts = None
        per_bus_values: dict[str, list[float]] = defaultdict(list)

        for r in rows:
            ts = r["ts"]
            val = r["occupancy_pct"]

            if ts is not None and (last_ts is None or ts > last_ts):
                last_ts = ts
            if val is not None:
                per_bus_values[r["device_id"]].append(float(val))

        bus_avgs = [sum(v) / len(v) for v in per_bus_values.values() if v]

        occupancy_avg = None
        if bus_avgs:
            occupancy_avg = round(sum(bus_avgs) / len(bus_avgs), 2)

        return {
            "asof": last_ts,
            "occupancy_avg": occupancy_avg,
        }

    async def add_measurement(
            self,
            camera_id: int,
            ts: datetime | None,
            occupancy_pct: float,
    ) -> dict:
        sql = """
            INSERT INTO info_from_camera (camera_id, ts, occupancy_pct)
            VALUES ($1, COALESCE($2, NOW()), $3)
            RETURNING id, camera_id, ts, occupancy_pct, created_at
        """

        if ts is not None and ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)

        row = await self.db.fetchrow(sql, camera_id, ts, occupancy_pct)

        return dict(row)

    async def get_measurements(
            self,
            camera_id: int,
            ts_from: Optional[datetime] = None,
            ts_to: Optional[datetime] = None,
            limit: Optional[int] = None,
            asc: bool = True,
    ) -> List[asyncpg.Record]:
        conds = ["camera_id = $1"]
        args = [camera_id]
        argi = 2

        if ts_from is not None:
            conds.append(f"ts >= ${argi}")
            args.append(ts_from)
            argi += 1

        if ts_to is not None:
            conds.append(f"ts <= ${argi}")
            args.append(ts_to)
            argi += 1

        order = "ASC" if asc else "DESC"
        lim = f" LIMIT {int(limit)}" if limit else ""

        sql = f"""
            SELECT id, camera_id, ts, occupancy_pct, created_at
            FROM info_from_camera
            WHERE {' AND '.join(conds)}
            ORDER BY ts {order}{lim}
        """

        return await self.db.fetch(sql, *args)
