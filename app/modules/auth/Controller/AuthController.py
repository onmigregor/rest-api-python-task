from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.modules.auth.Service.AuthService import AuthService
from app.modules.auth.Requests.AuthRequest import LoginRequest, LoginResponse, UserOut, RoleOut

class AuthController:
    @staticmethod
    def login(request: LoginRequest, db: Session = Depends(get_db)):
        user = AuthService.authenticate_user(db, request.email, request.password)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        roles = AuthService.get_user_roles(db, user.id)
        access_token, jti, expire = AuthService.create_access_token({"sub": str(user.id)})
        user_out = UserOut(
            id=user.id,
            name=user.name,
            email=user.email,
            roles=[RoleOut(id=role.id, name=role.name) for role in roles]
        )
        return {
            "data": {
                "token": access_token,
                "token_type": "Bearer",
                "user": user_out.model_dump(),
                "jti": jti,
                "expires_at": expire.isoformat()
            },
            "message": "Authenticated",
            "status": 200
        }

    @staticmethod
    def logout(request, db: Session = Depends(get_db)):
        """
        Logout real: revoca el token actual (lo guarda en la tabla revoked_tokens)
        """
        from fastapi import HTTPException, status
        from jose import jwt, JWTError
        from app.modules.auth.Service.AuthService import SECRET_KEY, ALGORITHM
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No token provided")
        token = auth_header.split(" ", 1)[1]
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            jti = payload.get("jti")
            user_id = int(payload.get("sub"))
            exp = payload.get("exp")
            if not jti or not exp:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")
            from datetime import datetime
            expires_at = datetime.utcfromtimestamp(exp)
            AuthService.revoke_token(db, token, jti, user_id, expires_at, reason="logout")
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return {"message": "Logout successful", "status": 200}
