from fastapi import Depends, status
from app.modules.auth.Dependencies.role_required import role_required
from app.config.route import get_module_router
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from app.config.database import get_db
from app.modules.user.Controller.UserController import UserController
from app.modules.user.Schemas.SchemasUser import UserCreate, UserUpdate

router = get_module_router("users")

@router.get("/", status_code=200)
def get_users(page: int = 1, limit: int = 10, db: Session = Depends(get_db), user_id: int = Depends(role_required(["Admin"]))):
    return UserController.get_users(page, limit, db)

@router.get("/{user_id}", status_code=200)
def get_user(user_id: int, db: Session = Depends(get_db), user_id_token: int = Depends(role_required(["Admin", "Single user"]))):
    return UserController.get_user(user_id, db)

@router.post("/", status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db), user_id: int = Depends(role_required(["Admin"]))):
    return UserController.create_user(user, db)

@router.put("/{user_id}", status_code=200)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db), user_id_token: int = Depends(role_required(["Admin"]))):
    return UserController.update_user(user_id, user, db)

@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db), user_id_token: int = Depends(role_required(["Admin"]))):
    return UserController.delete_user(user_id, db)
