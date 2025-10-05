from collections import defaultdict
from fastapi import APIRouter, Depends, HTTPException, Query
from apps.api.schemas import BusSnapshots, BusSnapshot
from apps.api.deps import get_info_manager

router = APIRouter(prefix="/bus", tags=["snapshots"])


@router.get("/now", response_model=BusSnapshots, summary="Данные по нескольким device_id")
async def buses_now(
        device_ids: list[str] = Query(..., description="Список device_id автобусов"),
        info=Depends(get_info_manager),
):
    rows = await info.fetch_snapshot_by_device_ids(device_ids)
    if not rows:
        raise HTTPException(404, detail="No data for given device_ids")
    result: dict[str, dict] = defaultdict(lambda: {"ts": None, "values": []})
    for r in rows:
        did, ts, occ = r["device_id"], r["ts"], r["occupancy_pct"]
        if occ is not None:
            result[did]["values"].append(round(float(occ), 2))
        if ts is not None and (result[did]["ts"] is None or ts > result[did]["ts"]):
            result[did]["ts"] = ts
    return result


@router.get("/now/{device_id}", response_model=BusSnapshot, summary="Данные по одному device_id")
async def bus_now_single(
        device_id: str,
        info=Depends(get_info_manager),
):
    rows = await info.fetch_snapshot_by_device_ids([device_id])
    if not rows:
        raise HTTPException(404, detail="Device not found or no data")
    ts = None
    values: list[float] = []
    for r in rows:
        if r["occupancy_pct"] is not None:
            values.append(round(float(r["occupancy_pct"]), 2))
        if r["ts"] is not None and (ts is None or r["ts"] > ts):
            ts = r["ts"]
    if not values and ts is None:
        raise HTTPException(404, detail="No data for this device")
    return BusSnapshot(ts=ts, values=values)
