from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.modules.task.Service.TaskService import TaskService
from app.modules.task.Requests.TaskRequest import TaskCreateRequest, TaskUpdateRequest
from app.modules.task.Schemas.TaskSchemas import TaskStatisticsOut, CategoryOut
from app.modules.task.Requests.TaskRequest import TaskStatisticsRequest
from app.modules.task.Resource.TaskResource import TaskResource
from typing import List

class TaskController:
    @staticmethod
    def _to_taskout_dict(task):
        d = {c.name: getattr(task, c.name) for c in task.__table__.columns}
        d["priority"] = d["priority"].value if d["priority"] else None
        return d

    @staticmethod
    def get_all(
        page: int, 
        limit: int, 
        db: Session, 
        current_user_id: int,
        is_admin: bool,
        query: str = None
    ):
        paginated_data = TaskService.get_all(
            db=db,
            page=page,
            limit=limit,
            current_user_id=current_user_id,
            is_admin=is_admin,
            query=query
        )
        return {"message": "success", "data": paginated_data}

    @staticmethod
    def get_by_id(task_id: int, db: Session):
        task = TaskService.get_by_id(db, task_id)
        return {"message": "success", "data": TaskResource.serialize(task)}

    @staticmethod
    def create(task: TaskCreateRequest, db: Session, user_id: int):
        from pydantic import ValidationError
        from fastapi.responses import JSONResponse
        try:
            task_obj = TaskService.create(db, task, user_id)
            return {"message": "success", "data": TaskResource.serialize(task_obj)}
        except ValidationError as e:
            return JSONResponse(status_code=422, content={"message": e.errors(), "status": 422})
        except Exception as e:
            # Si es HTTPException, formatear igual
            from fastapi import HTTPException
            if isinstance(e, HTTPException):
                return JSONResponse(status_code=e.status_code, content={"message": e.detail, "status": e.status_code})
            raise

    @staticmethod
    def update(task_id: int, task: TaskUpdateRequest, db: Session, user_id_token: int):
        from pydantic import ValidationError
        from fastapi.responses import JSONResponse
        try:
            task_obj = TaskService.update(db, task_id, task, user_id_token)
            return {"message": "success", "data": TaskResource.serialize(task_obj)}
        except ValidationError as e:
            return JSONResponse(status_code=422, content={"message": e.errors(), "status": 422})
        except Exception as e:
            from fastapi import HTTPException
            if isinstance(e, HTTPException):
                return JSONResponse(status_code=e.status_code, content={"message": e.detail, "status": e.status_code})
            raise

    @staticmethod
    def delete(task_id: int, db: Session):
        TaskService.delete(db, task_id)
        return {"message": "success", "data": None}

    @staticmethod
    def statistics(db: Session, params: TaskStatisticsRequest):
        try:
            stats = TaskService.statistics(
                db=db,
                start_date=params.start_date,
                end_date=params.end_date,
                user_id=params.user_id
            )
            return {"message": "success", "data": TaskStatisticsOut(**stats)}
        except HTTPException as e:
            # Re-lanzar las excepciones HTTP
            raise e
        except Exception as e:
            # Capturar cualquier otro error inesperado
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred while retrieving statistics: {str(e)}"
            )

    @staticmethod
    def get_categories(db: Session):
        categories = TaskService.get_categories(db)
        return {"message": "success", "data": [CategoryOut.model_validate(cat) for cat in categories]}
