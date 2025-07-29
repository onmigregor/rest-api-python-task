from fastapi import APIRouter, Depends
from app.modules.auth.Dependencies.role_required import role_required
from app.modules.category.Controller.CategoryController import CategoryController
from app.modules.category.Requests.CategoryRequest import CategoryCreateRequest, CategoryUpdateRequest, CategoryOutResponse, SuccessResponse, NotFoundResponse
from typing import List

router = APIRouter(prefix="/api/v1/categories", tags=["Category"])

from app.config.database import get_db

from fastapi import Query

@router.get("/", status_code=200)
def get_all(page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=100), db=Depends(get_db), user_id: int = Depends(role_required(["Admin", "Single user"]))):
    """
    Lista categorías de forma paginada. Usa los parámetros page y limit.
    """
    return CategoryController.get_all(db, page=page, limit=limit)

@router.get("/{category_id}", status_code=200)
def get_by_id(category_id: int, db=Depends(get_db), user_id: int = Depends(role_required(["Admin", "Single user"]))):
    """
    Consulta una categoría por id.
    """
    return CategoryController.get_by_id(category_id, db)

@router.post("/", status_code=201)
def create(category: CategoryCreateRequest, db=Depends(get_db), user_id: int = Depends(role_required(["Admin", "Single user"]))):
    """
    Crea una nueva categoría. El campo name es requerido y debe tener al menos 3 caracteres.
    """
    return CategoryController.create(category, db)

@router.put("/{category_id}", status_code=200)
def update(category_id: int, category_update: CategoryUpdateRequest, db=Depends(get_db), user_id: int = Depends(role_required(["Admin", "Single user"]))):
    """
    Actualiza una categoría. El campo name es requerido y debe tener al menos 3 caracteres.
    """
    return CategoryController.update(category_id, category_update, db)

@router.delete("/{category_id}", status_code=204)
def delete(category_id: int, db=Depends(get_db), user_id: int = Depends(role_required(["Admin"]))):
    """
    Elimina (borrado lógico) una categoría por id.
    Solo Admin puede eliminar.
    """
    CategoryController.delete(category_id, db)
    return None
