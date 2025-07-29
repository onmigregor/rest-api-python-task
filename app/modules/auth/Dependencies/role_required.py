from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.modules.auth.Dependencies.auth_jwt import get_current_user
from app.modules.user.Models.user import User
from app.modules.auth.Models.role import Role
from app.modules.auth.Models.user_role import UserRole
from app.config.database import get_db

def role_required(required_roles: list):
    def dependency(request: Request, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        # Obtener roles del usuario
        roles = (
            db.query(Role)
            .join(UserRole, UserRole.role_id == Role.id)
            .filter(UserRole.user_id == user.id)
            .all()
        )
        role_names = [r.name for r in roles]
        if not any(r in role_names for r in required_roles):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return user_id
    return dependency
