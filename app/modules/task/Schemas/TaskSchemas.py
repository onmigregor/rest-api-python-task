from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
from enum import Enum

class PriorityEnum(str, Enum):
    high = "high"
    medium = "medium"
    low = "low"

class TaskCreateRequest(BaseModel):
    title: str = Field(..., min_length=3, max_length=255)
    description: Optional[str] = Field(None, max_length=1024)
    due_date: Optional[datetime]
    priority: PriorityEnum = Field(...)
    category_id: int = Field(..., gt=0)
    assigned_to: Optional[int] = Field(None, gt=0)

class TaskUpdateRequest(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=255)
    description: Optional[str] = Field(None, max_length=1024)
    due_date: Optional[datetime]
    priority: Optional[PriorityEnum]
    category_id: Optional[int] = Field(None, gt=0)
    completed: Optional[bool]
    assigned_to: Optional[int] = Field(None, gt=0)

from pydantic import field_serializer

class TaskOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    completed: bool
    due_date: Optional[datetime]
    priority: str
    category_id: int
    created_by: int
    assigned_to: Optional[int]
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }

class TaskStatisticsOut(BaseModel):
    total: int
    completed: int
    pending: int

class CategoryOut(BaseModel):
    id: int
    name: str

    model_config = {
        "from_attributes": True
    }
