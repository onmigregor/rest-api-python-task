from fastapi import APIRouter, Depends, Request
from app.modules.auth.Controller.AuthController import AuthController
from app.modules.auth.Requests.AuthRequest import LoginRequest
from sqlalchemy.orm import Session
from app.config.database import get_db

router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])

@router.post("/login", status_code=200)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    Login de usuario. Devuelve JWT y datos del usuario con roles.
    """
    return AuthController.login(request, db)

@router.post("/logout", status_code=200, summary="Logout", description="Revoca el token JWT del usuario actual. No requiere body, solo el header Authorization.")
def logout(request: Request, db: Session = Depends(get_db)):
    """
    Logout de usuario. Revoca el token actual (lo guarda en la tabla revoked_tokens).
    Solo requiere el header Authorization: Bearer <token>.
    """
    return AuthController.logout(request, db)
