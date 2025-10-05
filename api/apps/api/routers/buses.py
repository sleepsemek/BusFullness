from fastapi import APIRouter, Depends
from apps.api.schemas import BusOut
from database.managers.bus_manager import BusManager
from apps.api.deps import get_bus_manager

router = APIRouter(prefix="/buses", tags=["buses"])


@router.get("", response_model=list[BusOut], summary="Список автобусов")
async def list_buses(bus_manager: BusManager = Depends(get_bus_manager)):
    items = await bus_manager.list_buses()
    return [BusOut.model_validate(dc, from_attributes=True) for dc in items]
