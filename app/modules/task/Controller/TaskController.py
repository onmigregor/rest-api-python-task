from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.modules.task.Service.TaskService import TaskService
from app.modules.task.Requests.TaskRequest import TaskCreateRequest, TaskUpdateRequest
from app.modules.task.Schemas.TaskSchemas import TaskStatisticsOut, CategoryOut
from app.modules.task.Resource.TaskResource import TaskResource
from typing import List

class TaskController:
    @staticmethod
    def _to_taskout_dict(task):
        d = {c.name: getattr(task, c.name) for c in task.__table__.columns}
        d["priority"] = d["priority"].value if d["priority"] else None
        return d

    @staticmethod
    def get_all(page: int, limit: int, db: Session):
        paginated_data = TaskService.get_all(db, page=page, limit=limit)
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
    def statistics(db: Session):
        stats = TaskService.statistics(db)
        return {"message": "success", "data": TaskStatisticsOut(**stats)}

    @staticmethod
    def get_categories(db: Session):
        categories = TaskService.get_categories(db)
        return {"message": "success", "data": [CategoryOut.model_validate(cat) for cat in categories]}
