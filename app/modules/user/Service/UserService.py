from sqlalchemy.orm import Session
from app.modules.user.Models.user import User
from app.modules.user.Schemas.SchemasUser import UserCreate, UserUpdate, UserOut
from app.common.security import hash_password
from fastapi.responses import JSONResponse

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get_users(self, page: int = 1, limit: int = 10):
        query = self.db.query(User).filter(User.delete_at == None)
        total_items = query.count()
        total_pages = (total_items + limit - 1) // limit
        users = query.offset((page - 1) * limit).limit(limit).all()
        return {
            "page": page,
            "per_page": limit,
            "total_pages": total_pages,
            "total_items": total_items,
            "users": [UserOut.model_validate(u).dict() for u in users]
        }

    def get_user(self, user_id: int):
        user = self.db.query(User).filter(User.id == user_id, User.delete_at == None).first()
        if not user:
            return JSONResponse(status_code=404, content={"message": "User not found", "status": 404})
        return UserOut.model_validate(user)

    def create_user(self, user_data: UserCreate):
        if self.db.query(User).filter(User.email == user_data.email).first():
            return JSONResponse(status_code=422, content={"message": "Email is already registered", "status": 422})
        hashed_password = hash_password(user_data.password)
        db_user = User(name=user_data.name, email=user_data.email, password=hashed_password)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return UserOut.model_validate(db_user)

    def update_user(self, user_id: int, user_data: UserUpdate):
        db_user = self.db.query(User).filter(User.id == user_id).first()
        if not db_user:
            return JSONResponse(status_code=404, content={"message": "User not found", "status": 404})
        if user_data.name is not None:
            db_user.name = user_data.name
        if user_data.email is not None:
            if self.db.query(User).filter(User.email == user_data.email, User.id != user_id).first():
                return JSONResponse(status_code=422, content={"message": "Email is already registered", "status": 422})
            db_user.email = user_data.email
        if user_data.password is not None:
            db_user.password = hash_password(user_data.password)
        self.db.commit()
        self.db.refresh(db_user)
        return UserOut.model_validate(db_user)

    def delete_user(self, user_id: int):
        from datetime import datetime
        db_user = self.db.query(User).filter(User.id == user_id, User.delete_at == None).first()
        if not db_user:
            return JSONResponse(status_code=404, content={"message": "User not found", "status": 404})
        db_user.delete_at = datetime.utcnow()
        self.db.commit()
        return None
