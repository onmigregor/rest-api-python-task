from sqlalchemy.orm import Session
from app.modules.auth.Models.user_role import UserRole
from app.modules.auth.Models.role import Role


def is_admin(user_id: int, db: Session) -> bool:
    """
    Verifica si un usuario tiene rol de administrador
    """
    # Buscar si el usuario tiene el rol 'Admin'
    admin_role = db.query(Role).filter(Role.name == "Admin").first()
    if not admin_role:
        return False
    
    # Verificar si el usuario tiene este rol
    user_role = db.query(UserRole).filter(
        UserRole.user_id == user_id,
        UserRole.role_id == admin_role.id
    ).first()
    
    return user_role is not None
