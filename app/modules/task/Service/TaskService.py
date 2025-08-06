from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.modules.task.Models.task import Task, PriorityEnum
from app.modules.category.Models.category import Category
from app.modules.user.Models.user import User
from app.modules.task.Requests.TaskRequest import TaskCreateRequest, TaskUpdateRequest
from app.modules.task.DataTransferData.TaskData import TaskDTO
from app.helpers.auth_utils import is_admin
from typing import List
from sqlalchemy import or_

class TaskService:
    @staticmethod
    def get_all(
        db: Session, 
        page: int = 1, 
        limit: int = 10, 
        current_user_id: int = None,
        is_admin: bool = False,
        query: str = None
    ):
        from sqlalchemy.orm import joinedload
        from app.modules.task.Resource.TaskResource import TaskResource
        
        # Construir query base con joins
        base_query = db.query(Task).options(
            joinedload(Task.category),
            joinedload(Task.creator),
            joinedload(Task.assignee)
        )
        
        # Aplicar filtro por usuario si no es admin
        if not is_admin:
            base_query = base_query.filter(
                or_(
                    Task.created_by == current_user_id,
                    Task.assigned_to == current_user_id
                )
            )
        
        # Aplicar filtro de búsqueda
        if query:
            search = f"%{query}%"
            base_query = base_query.filter(
                or_(
                    Task.title.ilike(search),
                    Task.description.ilike(search)
                )
            )
        
        # Calcular paginación
        total_items = base_query.count()
        total_pages = (total_items + limit - 1) // limit
        
        # Aplicar paginación
        tasks = base_query.offset((page - 1) * limit).limit(limit).all()
        
        # Serializar resultados
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
        # Validar fecha de vencimiento
        if task_data.due_date and task_data.due_date < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"field": "due_date", "msg": "Due date cannot be in the past"}
            )
            
        # Preparar datos usando DTO
        task_data = TaskDTO(task_data, user_id, db).prepare_for_create()
        
        # Crear la tarea
        task = Task(
            title=task_data.title,
            description=task_data.description,
            due_date=task_data.due_date,
            priority=task_data.priority,
            category_id=task_data.category_id,
            assigned_to=task_data.assigned_to,
            created_by=user_id
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
            
        # Preparar datos usando DTO
        task_data = TaskDTO(task_data, user_id_token, db).prepare_for_update()
        
        # Actualizar campos
        field_names = ['title', 'description', 'due_date', 'priority', 'category_id', 'assigned_to', 'completed']
        for field in field_names:
            value = getattr(task_data, field, None)
            if value is not None:
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
    def statistics(db: Session, start_date=None, end_date=None, user_id=None):
        from app.modules.user.Models.user import User
        from fastapi import HTTPException, status
     
        
        # Validar que el usuario exista si se especifica un user_id
        if user_id is not None:
            user = db.query(User).filter(User.id == user_id, User.delete_at == None).first()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"User with id {user_id} not found"
                )
        
        # Base query
        base_query = db.query(Task)
        
        # Aplicar filtro por usuario si se especifica
        if user_id is not None:
            base_query = base_query.filter(Task.assigned_to == user_id)
        
        # Verificar si ambos parámetros están presentes y son iguales (mismo día)
        if start_date and end_date and start_date == end_date:
            # Caso especial: filtrar por un día específico
            from datetime import datetime, timedelta
            day_start = datetime.combine(start_date, datetime.min.time())
            day_end = datetime.combine(end_date, datetime.min.time()) + timedelta(days=1, seconds=-1)
            # Aplicar filtro para un día específico
            base_query = base_query.filter(Task.created_at.between(day_start, day_end))
        else:
            # Caso normal: filtrar por rango de fechas
            if start_date:
                # Para start_date, usamos la fecha a las 00:00:00 horas
                from datetime import datetime
                start_datetime = datetime.combine(start_date, datetime.min.time())
                base_query = base_query.filter(Task.created_at >= start_datetime)
            
            if end_date:
                # Para end_date, usamos la fecha a las 23:59:59 horas
                from datetime import datetime, timedelta
                # Añadimos un día y restamos 1 segundo para obtener el final del día
                end_datetime = datetime.combine(end_date, datetime.min.time()) + timedelta(days=1, seconds=-1)
                base_query = base_query.filter(Task.created_at <= end_datetime)

        # Obtener los conteos con los filtros aplicados
        total = base_query.count()
        completed = base_query.filter(Task.completed == True).count()
        pending = total - completed  # Más eficiente que hacer otra consulta
        
        return {"total": total, "completed": completed, "pending": pending}

    @staticmethod
    def get_categories(db: Session):
        return db.query(Category).all()
