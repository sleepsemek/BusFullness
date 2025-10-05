from fastapi import APIRouter, Depends, HTTPException
from apps.api.schemas import RouteAvgOut
from database.managers.info_from_camera_manager import InfoFromCameraManager
from apps.api.deps import get_info_manager

router = APIRouter(prefix="/route", tags=["routes"])


@router.get("/avg/{route_id}", response_model=RouteAvgOut, summary="Средняя загрузка по маршруту")
async def route_avg(route_id: str, info: InfoFromCameraManager = Depends(get_info_manager)):
    row = await info.fetch_route_avg(route_id)
    if not row:
        raise HTTPException(404, "Route not found or no data")
    return RouteAvgOut(**row)
