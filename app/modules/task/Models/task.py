from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, ForeignKey, func
from sqlalchemy.orm import relationship
from app.config.database import Base
import enum

class PriorityEnum(enum.Enum):
    high = "high"
    medium = "medium"
    low = "low"

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(String(1024), nullable=True)
    completed = Column(Boolean, default=False)
    due_date = Column(DateTime, nullable=True)
    priority = Column(Enum(PriorityEnum), nullable=False, default=PriorityEnum.medium)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    category = relationship("Category", backref="tasks")
    creator = relationship("User", foreign_keys=[created_by])
    assignee = relationship("User", foreign_keys=[assigned_to])
