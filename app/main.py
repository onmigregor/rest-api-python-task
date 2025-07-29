from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from app.modules.user.Routes.api import router as users_router
from app.modules.category.Routes.api import router as category_router
from app.core.ExceptionValidator.index import validation_exception_handler, pydantic_validation_exception_handler

app = FastAPI(
    title="Task Manager API",
    description="API modular para gestión de tareas",
    version="0.1.0"
)

@app.exception_handler(RequestValidationError)
async def _validation_exception_handler(request, exc):
    return await validation_exception_handler(request, exc)

@app.exception_handler(ValidationError)
async def _pydantic_validation_exception_handler(request, exc):
    return await pydantic_validation_exception_handler(request, exc)

app.include_router(users_router)
app.include_router(category_router)

@app.get("/")
def read_root():
    return {"msg": "Welcome to Task Manager API"}
