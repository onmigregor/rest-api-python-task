from sqlalchemy.orm import Session
from app.modules.category.Models.category import Category
from app.modules.category.Requests.CategoryRequest import CategoryCreateRequest, CategoryUpdateRequest
from typing import List, Optional
from datetime import datetime

class CategoryService:
    @staticmethod
    def get_all(db: Session, page: int = 1, limit: int = 10):
        from app.modules.category.Requests.CategoryRequest import CategoryOutResponse
        query = db.query(Category).filter(Category.delete_at == None)
        total_items = query.count()
        total_pages = (total_items + limit - 1) // limit if limit else 1
        items = query.offset((page - 1) * limit).limit(limit).all()
        return {
            "page": page,
            "per_page": limit,
            "total_pages": total_pages,
            "total_items": total_items,
            "categories": [CategoryOutResponse.model_validate(item).model_dump() for item in items]
        }

    @staticmethod
    def get_by_id(db: Session, category_id: int):
        from app.modules.category.Requests.CategoryRequest import CategoryOutResponse
        cat = db.query(Category).filter(Category.id == category_id, Category.delete_at == None).first()
        if not cat:
            return None
        return CategoryOutResponse.model_validate(cat).model_dump()

    @staticmethod
    def create(db: Session, category: CategoryCreateRequest):
        from app.modules.category.Requests.CategoryRequest import CategoryOutResponse
        exists = db.query(Category).filter(
            Category.name == category.name,
            Category.delete_at == None
        ).first()
        if exists:
            raise ValueError("El nombre de la categoría ya existe")
        db_category = Category(**category.model_dump())
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return CategoryOutResponse.model_validate(db_category).model_dump()

    @staticmethod
    def update(db: Session, category_id: int, category_update: CategoryUpdateRequest):
        from sqlalchemy.exc import IntegrityError
        from app.modules.category.Requests.CategoryRequest import CategoryOutResponse
        db_category = db.query(Category).filter(Category.id == category_id, Category.delete_at == None).first()
        if not db_category:
            return None
        # Si se quiere actualizar el nombre, validar unicidad
        if category_update.name and category_update.name != db_category.name:
            exists = db.query(Category).filter(
                Category.name == category_update.name,
                Category.delete_at == None,
                Category.id != category_id
            ).first()
            if exists:
                raise ValueError("El nombre de la categoría ya existe")
        for field, value in category_update.model_dump(exclude_unset=True).items():
            setattr(db_category, field, value)
        db_category.updated_at = datetime.utcnow()
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise ValueError("El nombre de la categoría ya existe")
        db.refresh(db_category)
        return CategoryOutResponse.model_validate(db_category).model_dump()

    @staticmethod
    def delete(db: Session, category_id: int) -> bool:
        db_category = db.query(Category).filter(Category.id == category_id, Category.delete_at == None).first()
        if not db_category:
            return False
        db_category.delete_at = datetime.utcnow()
        db.commit()
        return True
