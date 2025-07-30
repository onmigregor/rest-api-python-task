from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.config.database import get_db
from app.modules.task.Controller.TaskController import TaskController
from app.modules.task.Requests.TaskRequest import TaskCreateRequest, TaskUpdateRequest
from app.modules.task.Schemas.TaskSchemas import TaskOut, TaskStatisticsOut, CategoryOut
from app.modules.auth.Dependencies.auth_jwt import get_current_user
from app.modules.auth.Dependencies.role_required import role_required

router = APIRouter(prefix="/api/v1/tasks", tags=["Task"])

@router.get("/", status_code=200)
def get_tasks(page: int = 1, limit: int = 10, db: Session = Depends(get_db), user_id_token: int = Depends(role_required(["Admin", "User"]))):
    return TaskController.get_all(page, limit, db)

@router.get("/statistics", status_code=200)
def get_statistics(db: Session = Depends(get_db), user_id_token: int = Depends(role_required(["Admin", "User"]))):
    return TaskController.statistics(db)

@router.get("/categories", status_code=200)
def get_categories(db: Session = Depends(get_db), user_id_token: int = Depends(role_required(["Admin", "User"]))):
    return TaskController.get_categories(db)

@router.get("/{task_id}", status_code=200)
def get_task(task_id: int, db: Session = Depends(get_db), user_id_token: int = Depends(role_required(["Admin", "User"]))):
    return TaskController.get_by_id(task_id, db)

@router.post("/", status_code=201)
def create_task(task: TaskCreateRequest, db: Session = Depends(get_db), user_id_token: int = Depends(role_required(["Admin", "User"]))):
    return TaskController.create(task, db, user_id_token)

@router.put("/{task_id}", status_code=200)
def update_task(task_id: int, task: TaskUpdateRequest, db: Session = Depends(get_db), user_id_token: int = Depends(role_required(["Admin", "User"]))):
    return TaskController.update(task_id, task, db, user_id_token)

@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db), user_id_token: int = Depends(role_required(["Admin"]))):
    TaskController.delete(task_id, db)
    return None
