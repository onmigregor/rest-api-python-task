from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.modules.category.Models.category import Category
from app.modules.user.Models.user import User

class TaskValidator:
    @staticmethod
    def validate_category(db: Session, category_id: int):
        """Valida que la categoría exista"""
        if category_id is not None:
            category = db.query(Category).get(category_id)
            if not category:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={"field": "category_id", "msg": "Category does not exist"}
                )

    @staticmethod
    def validate_assigned_user(db: Session, assigned_to: int):
        """Valida que el usuario asignado exista"""
        if assigned_to is not None:
            user = db.query(User).get(assigned_to)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={"field": "assigned_to", "msg": "Assigned user does not exist"}
                )

    @staticmethod
    def auto_assign_if_not_admin(db: Session, user_id: int, task_data):
        """Autoasigna la tarea al usuario actual si no es admin"""
        from app.helpers.auth_utils import is_admin
        if not is_admin(user_id, db):
            task_data.assigned_to = user_id
        return task_data
