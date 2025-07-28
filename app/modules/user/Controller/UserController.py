from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.modules.user.Service.UserService import UserService
from app.modules.user.Schemas.SchemasUser import UserCreate, UserUpdate

class UserController:
    @staticmethod
    def get_users(page: int, limit: int, db: Session):
        service = UserService(db)
        data = service.get_users(page=page, limit=limit)
        return {"message": "success", "data": data}

    @staticmethod
    def get_user(user_id: int, db: Session):
        service = UserService(db)
        result = service.get_user(user_id)
        if isinstance(result, JSONResponse):
            return result
        return {"message": "success", "data": result}

    @staticmethod
    def create_user(user: UserCreate, db: Session):
        service = UserService(db)
        result = service.create_user(user)
        if isinstance(result, JSONResponse):
            return result
        return {"message": "success", "data": result}

    @staticmethod
    def update_user(user_id: int, user: UserUpdate, db: Session):
        service = UserService(db)
        result = service.update_user(user_id, user)
        if isinstance(result, JSONResponse):
            return result
        return {"message": "success", "data": result}

    @staticmethod
    def delete_user(user_id: int, db: Session):
        service = UserService(db)
        result = service.delete_user(user_id)
        if isinstance(result, JSONResponse):
            return result
        return None
