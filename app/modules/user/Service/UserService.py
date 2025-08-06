from sqlalchemy.orm import Session, joinedload
from app.modules.user.Models.user import User
from app.modules.user.Schemas.SchemasUser import UserCreate, UserUpdate, UserOut, RoleOut
from app.modules.auth.Models.role import Role
from app.modules.auth.Models.user_role import UserRole
from app.common.security import hash_password
from fastapi.responses import JSONResponse

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def _validate_role_exists(self, role_id: int):
        """Valida que el rol exista en la base de datos"""
        role = self.db.query(Role).filter(Role.id == role_id).first()
        if not role:
            return JSONResponse(
                status_code=422, 
                content={"message": f"Role with id {role_id} does not exist", "status": 422}
            )
        return role

    def _get_user_with_roles(self, user_id: int):
        """Obtiene un usuario con sus roles cargados"""
        user = self.db.query(User).filter(User.id == user_id, User.delete_at == None).first()
        if not user:
            return None
        
        # Obtener roles del usuario
        roles = (
            self.db.query(Role)
            .join(UserRole, UserRole.role_id == Role.id)
            .filter(UserRole.user_id == user_id)
            .all()
        )
        
        # Crear objeto UserOut con roles
        user_dict = {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "roles": [{"id": role.id, "name": role.name} for role in roles]
        }
        return UserOut(**user_dict)

    def get_all_users(self):
        """Obtiene todos los usuarios del sistema sin paginación"""
        users = self.db.query(User).filter(User.delete_at == None).all()
        
        # Obtener usuarios con sus roles
        users_with_roles = []
        for user in users:
            user_with_roles = self._get_user_with_roles(user.id)
            if user_with_roles:
                users_with_roles.append(user_with_roles.model_dump())
        
        return users_with_roles

    def get_users(self, page: int = 1, limit: int = 10):
        query = self.db.query(User).filter(User.delete_at == None)
        total_items = query.count()
        total_pages = (total_items + limit - 1) // limit
        users = query.offset((page - 1) * limit).limit(limit).all()
        
        # Obtener usuarios con sus roles
        users_with_roles = []
        for user in users:
            user_with_roles = self._get_user_with_roles(user.id)
            if user_with_roles:
                users_with_roles.append(user_with_roles.model_dump())
        
        return {
            "page": page,
            "per_page": limit,
            "total_pages": total_pages,
            "total_items": total_items,
            "users": users_with_roles
        }

    def get_user(self, user_id: int):
        user_with_roles = self._get_user_with_roles(user_id)
        if not user_with_roles:
            return JSONResponse(status_code=404, content={"message": "User not found", "status": 404})
        return user_with_roles

    def create_user(self, user_data: UserCreate):
        # Validar que el email no esté registrado
        if self.db.query(User).filter(User.email == user_data.email).first():
            return JSONResponse(status_code=422, content={"message": "Email is already registered", "status": 422})
        
        # Validar que el rol existe
        role_validation = self._validate_role_exists(user_data.role_id)
        if isinstance(role_validation, JSONResponse):
            return role_validation
        
        # Crear usuario
        hashed_password = hash_password(user_data.password)
        db_user = User(name=user_data.name, email=user_data.email, password=hashed_password)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        
        # Asignar rol al usuario
        user_role = UserRole(user_id=db_user.id, role_id=user_data.role_id)
        self.db.add(user_role)
        self.db.commit()
        
        return self._get_user_with_roles(db_user.id)

    def update_user(self, user_id: int, user_data: UserUpdate):
        db_user = self.db.query(User).filter(User.id == user_id).first()
        if not db_user:
            return JSONResponse(status_code=404, content={"message": "User not found", "status": 404})
        
        # Validar rol si se proporciona
        if user_data.role_id is not None:
            role_validation = self._validate_role_exists(user_data.role_id)
            if isinstance(role_validation, JSONResponse):
                return role_validation
        
        # Actualizar campos del usuario
        if user_data.name is not None:
            db_user.name = user_data.name
        if user_data.email is not None:
            if self.db.query(User).filter(User.email == user_data.email, User.id != user_id).first():
                return JSONResponse(status_code=422, content={"message": "Email is already registered", "status": 422})
            db_user.email = user_data.email
        if user_data.password is not None:
            db_user.password = hash_password(user_data.password)
        
        # Actualizar rol si se proporciona
        if user_data.role_id is not None:
            # Eliminar roles existentes
            self.db.query(UserRole).filter(UserRole.user_id == user_id).delete()
            # Asignar nuevo rol
            user_role = UserRole(user_id=user_id, role_id=user_data.role_id)
            self.db.add(user_role)
        
        self.db.commit()
        self.db.refresh(db_user)
        return self._get_user_with_roles(user_id)

    def delete_user(self, user_id: int):
        from datetime import datetime
        db_user = self.db.query(User).filter(User.id == user_id, User.delete_at == None).first()
        if not db_user:
            return JSONResponse(status_code=404, content={"message": "User not found", "status": 404})
        db_user.delete_at = datetime.utcnow()
        self.db.commit()
        return None
