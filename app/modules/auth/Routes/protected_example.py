from fastapi import APIRouter, Depends
from app.modules.auth.Dependencies.auth_jwt import get_current_user

router = APIRouter(prefix="/api/v1/protected", tags=["Protected"])

@router.get("/me")
def get_me(user_id: int = Depends(get_current_user)):
    """
    Ruta protegida de ejemplo. Solo accesible con JWT válido y no revocado.
    """
    return {"message": "Acceso permitido", "user_id": user_id}
