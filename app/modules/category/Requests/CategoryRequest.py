from pydantic import BaseModel, Field, model_validator
from typing import Optional
from sqlalchemy.orm import Session
from app.modules.category.Models.category import Category

class CategoryCreateRequest(BaseModel):
    """
    Request para crear categoría. El campo name es requerido y debe tener al menos 3 caracteres.
    """
    name: str = Field(..., min_length=3, max_length=100, example="Trabajo")
    description: Optional[str] = Field(None, max_length=255, example="Tareas laborales")

    @model_validator(mode="after")
    def name_must_be_unique(self):
        # Este validador requiere que se le pase un Session manualmente si se usa así
        # La validación real de unicidad debe hacerse en el servicio
        return self

class CategoryUpdateRequest(BaseModel):
    """
    Request para actualizar categoría. El campo name es requerido y debe tener al menos 3 caracteres.
    """
    name: str = Field(..., min_length=3, max_length=100, example="Trabajo")
    description: Optional[str] = Field(None, max_length=255, example="Tareas laborales")

class CategoryOutResponse(BaseModel):
    """
    Respuesta de salida para categorías.
    """
    id: int
    name: str
    description: Optional[str] = None
    class Config:
        from_attributes = True

class SuccessResponse(BaseModel):
    """
    Respuesta de éxito estándar.
    """
    message: str = "success"
    data: object

class NotFoundResponse(BaseModel):
    message: str = "Not found"
    status: int = 404
