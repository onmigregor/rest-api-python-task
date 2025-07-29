from sqlalchemy.orm import Session
from app.modules.user.Models.user import User
from app.modules.auth.Models.role import Role
from app.modules.auth.Models.user_role import UserRole
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
import os
import uuid
from app.modules.auth.Models.revoked_token import RevokedToken

SECRET_KEY = os.getenv("SECRET_KEY", "myjwtsecret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    @staticmethod
    def authenticate_user(db: Session, email: str, password: str):
        user = db.query(User).filter(User.email == email, User.delete_at == None).first()
        if not user or not pwd_context.verify(password, user.password):
            return None
        return user

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        jti = str(uuid.uuid4())
        to_encode.update({"exp": expire, "jti": jti})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM), jti, expire

    @staticmethod
    def revoke_token(db: Session, token: str, jti: str, user_id: int, expires_at: datetime, reason: str = None):
        # Evita error en logout doble: si ya está revocado, ignora
        exists = db.query(RevokedToken).filter_by(jti=jti).first()
        if exists:
            return
        revoked = RevokedToken(jti=jti, token=token, user_id=user_id, expires_at=expires_at, reason=reason)
        db.add(revoked)
        db.commit()

    @staticmethod
    def is_token_revoked(db: Session, jti: str) -> bool:
        return db.query(RevokedToken).filter_by(jti=jti).first() is not None

    @staticmethod
    def get_user_roles(db: Session, user_id: int):
        roles = (
            db.query(Role)
            .join(UserRole, UserRole.role_id == Role.id)
            .filter(UserRole.user_id == user_id)
            .all()
        )
        return roles
