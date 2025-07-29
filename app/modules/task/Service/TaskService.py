from sqlalchemy.orm import Session
from app.modules.task.Models.task import Task, PriorityEnum
from app.modules.category.Models.category import Category
from app.modules.user.Models.user import User
from app.modules.task.Requests.TaskRequest import TaskCreateRequest, TaskUpdateRequest
from fastapi import HTTPException, status
from typing import List

class TaskService:
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 10) -> List[Task]:
        from sqlalchemy.orm import joinedload
        return db.query(Task)\
            .options(
                joinedload(Task.category),
                joinedload(Task.creator),
                joinedload(Task.assignee)
            )\
            .offset(skip)\
            .limit(limit)\
            .all()

    @staticmethod
    def get_by_id(db: Session, task_id: int) -> Task:
        from sqlalchemy.orm import joinedload
        task = db.query(Task) \
            .options(
                joinedload(Task.category),
                joinedload(Task.creator),
                joinedload(Task.assignee)
            ) \
            .filter(Task.id == task_id).first()
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        return task

    @staticmethod
    def create(db: Session, task_data: TaskCreateRequest, user_id: int) -> Task:
        # Validar existencia de category y assigned_to
        category = db.query(Category).filter(Category.id == task_data.category_id).first()
        if not category:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category does not exist")
        if task_data.assigned_to:
            assigned_user = db.query(User).filter(User.id == task_data.assigned_to).first()
            if not assigned_user:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"field": "assigned_to", "msg": "Assigned user does not exist"})
            if task_data.assigned_to == user_id:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"field": "assigned_to", "msg": "The creator cannot assign the task to themselves"})
        # Validar que due_date no sea pasada
        from datetime import datetime
        if task_data.due_date and task_data.due_date < datetime.now():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"field": "due_date", "msg": "Due date cannot be in the past"})
        task = Task(
            title=task_data.title,
            description=task_data.description,
            due_date=task_data.due_date,
            priority=task_data.priority,
            category_id=task_data.category_id,
            created_by=user_id,
            assigned_to=task_data.assigned_to
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        return task

    @staticmethod
    def update(db: Session, task_id: int, task_data: TaskUpdateRequest, user_id_token: int) -> Task:
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

        # Validar existencia de category_id si se va a actualizar
        if task_data.category_id is not None:
            category = db.query(Category).filter(Category.id == task_data.category_id).first()
            if not category:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"field": "category_id", "msg": "Category does not exist"})

        # Validar existencia de assigned_to si se va a actualizar
        if task_data.assigned_to is not None:
            assigned_user = db.query(User).filter(User.id == task_data.assigned_to).first()
            if not assigned_user:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"field": "assigned_to", "msg": "Assigned user does not exist"})

        for field, value in task_data.dict(exclude_unset=True).items():
            setattr(task, field, value)
        db.commit()
        db.refresh(task)
        return task

    @staticmethod
    def delete(db: Session, task_id: int):
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        db.delete(task)
        db.commit()

    @staticmethod
    def statistics(db: Session):
        total = db.query(Task).count()
        completed = db.query(Task).filter(Task.completed == True).count()
        pending = db.query(Task).filter(Task.completed == False).count()
        return {"total": total, "completed": completed, "pending": pending}

    @staticmethod
    def get_categories(db: Session):
        return db.query(Category).all()
