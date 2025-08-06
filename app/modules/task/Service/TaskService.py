from sqlalchemy.orm import Session
from app.modules.task.Models.task import Task, PriorityEnum
from app.modules.category.Models.category import Category
from app.modules.user.Models.user import User
from app.modules.task.Requests.TaskRequest import TaskCreateRequest, TaskUpdateRequest
from fastapi import HTTPException, status
from typing import List

class TaskService:
    @staticmethod
    def get_all(db: Session, page: int = 1, limit: int = 10):
        from sqlalchemy.orm import joinedload
        from app.modules.task.Resource.TaskResource import TaskResource
        
        # Construir query base con joins
        query = db.query(Task).options(
            joinedload(Task.category),
            joinedload(Task.creator),
            joinedload(Task.assignee)
        )
        
        # Calcular paginación
        total_items = query.count()
        total_pages = (total_items + limit - 1) // limit
        
        # Obtener tasks paginados
        tasks = query.offset((page - 1) * limit).limit(limit).all()
        
        # Serializar tasks
        serialized_tasks = [TaskResource.serialize(task) for task in tasks]
        
        return {
            "page": page,
            "per_page": limit,
            "total_pages": total_pages,
            "total_items": total_items,
            "tasks": serialized_tasks
        }

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
    def statistics(db: Session, start_date=None, end_date=None):
        # Base query
        base_query = db.query(Task)
        
        # Verificar si ambos parámetros están presentes y son iguales (mismo día)
        if start_date and end_date and start_date == end_date:
            # Caso especial: filtrar por un día específico
            from datetime import datetime, timedelta
            day_start = datetime.combine(start_date, datetime.min.time())
            day_end = datetime.combine(end_date, datetime.min.time()) + timedelta(days=1, seconds=-1)
            # Aplicar filtro para un día específico
            base_query = base_query.filter(Task.created_at >= day_start)
            base_query = base_query.filter(Task.created_at <= day_end)
        else:
            # Caso normal: filtrar por rango de fechas
            if start_date:
                # Para start_date, usamos la fecha a las 00:00:00 horas
                from datetime import datetime
                start_datetime = datetime.combine(start_date, datetime.min.time())
                print(f"DEBUG - Filtro start_datetime: {start_datetime}")
                base_query = base_query.filter(Task.created_at >= start_datetime)
            
            if end_date:
                # Para end_date, usamos la fecha a las 23:59:59 horas
                from datetime import datetime, timedelta
                # Añadimos un día y restamos 1 segundo para obtener el final del día
                end_datetime = datetime.combine(end_date, datetime.min.time()) + timedelta(days=1, seconds=-1)
                print(f"DEBUG - Filtro end_datetime: {end_datetime}")
                base_query = base_query.filter(Task.created_at <= end_datetime)

        # Contar totales con los filtros aplicados
        total = base_query.count()
        completed = base_query.filter(Task.completed == True).count()
        pending = base_query.filter(Task.completed == False).count()
        
        return {"total": total, "completed": completed, "pending": pending}

    @staticmethod
    def get_categories(db: Session):
        return db.query(Category).all()
