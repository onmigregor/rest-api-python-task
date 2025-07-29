from fastapi import Depends, HTTPException, status, Request
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.modules.auth.Service.AuthService import AuthService, SECRET_KEY, ALGORITHM

async def get_current_user(request: Request, db: Session = Depends(get_db)):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No token provided")
    token = auth_header.split(" ", 1)[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        jti = payload.get("jti")
        if AuthService.is_token_revoked(db, jti):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token revoked")
        user_id = int(payload.get("sub"))
        return user_id
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
