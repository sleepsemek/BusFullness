from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from apps.api.schemas import MeasurementOut, MeasurementIn
from database.managers.info_from_camera_manager import InfoFromCameraManager
from apps.api.deps import get_info_manager

router = APIRouter(prefix="/camera", tags=["measurements"])


@router.post(
    "/measurement",
    response_model=MeasurementOut,
    status_code=201,
    summary="Добавить измерение по camera_id",
)
async def add_measurement(
        camera_id: int,
        payload: MeasurementIn,
        info: InfoFromCameraManager = Depends(get_info_manager),
):
    occ = round(float(payload.occupancy_pct), 2)
    ts = payload.ts or datetime.utcnow()
    try:
        created = await info.add_measurement(camera_id=camera_id, ts=ts, occupancy_pct=occ)
    except KeyError:
        raise HTTPException(status_code=404, detail="Camera not found")
    return MeasurementOut(**created)


@router.get(
    "/measurements/{camera_id}",
    response_model=list[MeasurementOut],
    summary="Измерения камеры за интервал",
)
async def camera_measurements(
        camera_id: int,
        ts_from: Optional[datetime] = Query(None, description="ISO8601, напр. 2025-10-04T10:00:00Z"),
        ts_to: Optional[datetime] = Query(None, description="ISO8601"),
        limit: Optional[int] = Query(None, ge=1, le=10000),
        order: Optional[str] = Query("asc", pattern="^(?i)(asc|desc)$"),
        info: InfoFromCameraManager = Depends(get_info_manager),
):
    asc = (order or "asc").lower() == "asc"
    rows = await info.get_measurements(camera_id=camera_id, ts_from=ts_from, ts_to=ts_to, limit=limit, asc=asc)
    if not rows:
        raise HTTPException(status_code=404, detail="No measurements found")
    out = []
    for r in rows:
        d = dict(r)
        d["occupancy_pct"] = round(float(d["occupancy_pct"]), 2)
        out.append(MeasurementOut(**d))
    return out
