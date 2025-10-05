from fastapi import Request


def get_bus_manager(request: Request):
    return request.app.state.bus_manager


def get_camera_manager(request: Request):
    return request.app.state.camera_manager


def get_info_manager(request: Request):
    return request.app.state.info_from_camera_manager
