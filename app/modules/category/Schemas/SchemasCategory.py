from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class CategoryBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: Optional[str] = Field(None, max_length=255)

from pydantic import model_validator
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.modules.category.Models.category import Category

class CategoryCreate(CategoryBase):
    @model_validator(mode="after")
    def name_must_be_unique(self):
        # Este validador solo funcionará si se llama explícitamente con un db Session
        # Para validación real, debe hacerse en el servicio o controlador
        return self

class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=255)

class CategoryOut(CategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime
    delete_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
