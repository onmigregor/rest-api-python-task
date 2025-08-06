from pydantic import BaseModel, Field, field_validator, ValidationError, model_validator
from typing import Optional, Union
from datetime import datetime, date
from enum import Enum

class PriorityEnum(str, Enum):
    high = "high"
    medium = "medium"
    low = "low"

class TaskCreateRequest(BaseModel):
    title: str = Field(..., min_length=3, max_length=255, example="Título de la tarea")
    description: Optional[str] = Field(None, max_length=1024, example="Descripción de la tarea")
    due_date: Optional[datetime] = Field(None, example="2025/08/01")
    priority: PriorityEnum = Field(..., example="medium")
    category_id: int = Field(..., gt=0, example=1)
    assigned_to: Optional[int] = Field(None, gt=0, example=2)

    @field_validator('due_date', mode='before')
    def validate_due_date_format(cls, v):
        if v is None:
            return v
        if isinstance(v, datetime):
            return v
        try:
            # Solo acepta formato yyyy/mm/dd
            return datetime.strptime(v, "%Y/%m/%d")
        except Exception:
            raise ValueError("due_date have to have format yyyy/mm/dd")
        return v

class TaskUpdateRequest(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=255, example="Título de la tarea")
    description: Optional[str] = Field(None, max_length=1024, example="Descripción de la tarea")
    due_date: Optional[datetime] = Field(None, example="2025/08/01")
    priority: Optional[PriorityEnum] = Field(None, example="medium")
    category_id: Optional[int] = Field(None, gt=0, example=1)
    completed: Optional[bool] = Field(None, example=False)
    assigned_to: Optional[int] = Field(None, gt=0, example=2)

    @field_validator('due_date', mode='before')
    def validate_due_date_format(cls, v):
        if v is None:
            return v
        if isinstance(v, datetime):
            return v
        try:
            return datetime.strptime(v, "%Y/%m/%d")
        except Exception:
            raise ValueError("due_date have to have format yyyy/mm/dd")
        return v


class TaskStatisticsRequest(BaseModel):
    start_date: Optional[date] = Field(
        None, 
        description="Fecha de inicio para filtrar estadísticas (YYYY-MM-DD)"
    )
    end_date: Optional[date] = Field(
        None, 
        description="Fecha de fin para filtrar estadísticas (YYYY-MM-DD)"
    )
    user_id: Optional[int] = Field(
        None, 
        gt=0, 
        description="ID de usuario para filtrar tareas asignadas"
    )

    @model_validator(mode='after')
    def validate_dates(self):
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValueError("start_date cannot be greater than end_date")
        return self
