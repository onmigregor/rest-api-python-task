from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.modules.category.Service.CategoryService import CategoryService
from app.modules.category.Requests.CategoryRequest import CategoryCreateRequest, CategoryUpdateRequest, CategoryOutResponse, SuccessResponse, NotFoundResponse
from typing import List

class CategoryController:
    @staticmethod
    def get_all(db: Session, page: int = 1, limit: int = 10):
        data = CategoryService.get_all(db, page=page, limit=limit)
        return {"message": "success", "data": data}

    @staticmethod
    def get_by_id(category_id: int, db: Session = Depends(get_db)) -> dict:
        data = CategoryService.get_by_id(db, category_id)
        if not data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
        return {"message": "success", "data": data}

    @staticmethod
    def create(category: CategoryCreateRequest, db: Session = Depends(get_db)) -> dict:
        try:
            data = CategoryService.create(db, category)
            return {"message": "success", "data": data}
        except ValueError as e:
            from fastapi import HTTPException, status
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    @staticmethod
    def update(category_id: int, category_update: CategoryUpdateRequest, db: Session = Depends(get_db)) -> dict:
        try:
            data = CategoryService.update(db, category_id, category_update)
        except ValueError as e:
            from fastapi import HTTPException, status
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        if not data:
            from fastapi import HTTPException, status
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
        return {"message": "success", "data": data}

    @staticmethod
    def delete(category_id: int, db: Session = Depends(get_db)) -> None:
        deleted = CategoryService.delete(db, category_id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
        return None
