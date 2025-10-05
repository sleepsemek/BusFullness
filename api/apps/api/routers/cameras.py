from fastapi import APIRouter, Depends, HTTPException
from apps.api.schemas import CameraOut
from database.managers.camera_manager import CameraManager
from apps.api.deps import get_camera_manager

router = APIRouter(prefix="/bus", tags=["cameras"])


@router.get("/{device_id}/cameras", response_model=list[CameraOut], summary="Камеры автобуса")
async def list_bus_cameras(
        device_id: str,
        camera_manager: CameraManager = Depends(get_camera_manager),
):
    cams = await camera_manager.list_by_device_id(device_id)
    if not cams:
        raise HTTPException(404, detail="Bus not found or no cameras")
    return [CameraOut.model_validate(dc, from_attributes=True) for dc in cams]
