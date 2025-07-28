from fastapi import APIRouter

def get_module_router(module_name: str) -> APIRouter:
    """
    Devuelve un APIRouter con prefijo y tags estandarizados para el módulo.
    Ejemplo: get_module_router("users") genera prefix='/api/v1/users', tags=['users']
    """
    return APIRouter(
        prefix=f"/api/v1/{module_name}",
        tags=[module_name]
    )
