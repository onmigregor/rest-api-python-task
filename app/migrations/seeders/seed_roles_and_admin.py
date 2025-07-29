from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.modules.auth.Models.role import Role
from app.modules.auth.Models.user_role import UserRole
from app.modules.user.Models.user import User
from passlib.context import CryptContext
import os

# Configuración de conexión (ajusta si usas variables de entorno)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:123456@localhost/taskmanager")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def seed():
    session = SessionLocal()
    try:
        # Crear roles si no existen
        admin_role = session.query(Role).filter_by(name="Admin").first()
        if not admin_role:
            admin_role = Role(name="Admin")
            session.add(admin_role)
        user_role = session.query(Role).filter_by(name="Single user").first()
        if not user_role:
            user_role = Role(name="Single user")
            session.add(user_role)
        session.commit()

        # Crear usuario admin si no existe
        admin_user = session.query(User).filter_by(email="Admin@mail.com").first()
        if not admin_user:
            hashed_password = pwd_context.hash("12345678")
            admin_user = User(
                name="Admin",
                email="admin@mail.com",
                password=hashed_password
            )
            session.add(admin_user)
            session.commit()
        # Asignar rol Admin al usuario admin
        admin_user = session.query(User).filter_by(email="admin@mail.com").first()
        admin_role = session.query(Role).filter_by(name="Admin").first()
        user_role_link = session.query(UserRole).filter_by(user_id=admin_user.id, role_id=admin_role.id).first()
        if not user_role_link:
            session.add(UserRole(user_id=admin_user.id, role_id=admin_role.id))
        session.commit()

        # Crear usuario normal si no existe
        normal_user = session.query(User).filter_by(email="user@mail.com").first()
        if not normal_user:
            hashed_password = pwd_context.hash("123456")
            normal_user = User(
                name="User",
                email="user@mail.com",
                password=hashed_password
            )
            session.add(normal_user)
            session.commit()
        # Asignar rol Single user al usuario normal
        normal_user = session.query(User).filter_by(email="user@mail.com").first()
        single_role = session.query(Role).filter_by(name="Single user").first()
        user_role_link = session.query(UserRole).filter_by(user_id=normal_user.id, role_id=single_role.id).first()
        if not user_role_link:
            session.add(UserRole(user_id=normal_user.id, role_id=single_role.id))
        session.commit()
        print("Seed completado: roles, usuario admin y usuario normal creados.")
    finally:
        session.close()

if __name__ == "__main__":
    seed()
