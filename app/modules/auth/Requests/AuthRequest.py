from pydantic import BaseModel, Field
from typing import List, Optional

class LoginRequest(BaseModel):
    email: str = Field(..., example="Admin@mail.com")
    password: str = Field(..., example="12345678")

class RoleOut(BaseModel):
    id: int
    name: str

class UserOut(BaseModel):
    id: int
    name: str
    email: str
    roles: List[RoleOut]

class LoginResponse(BaseModel):
    data: dict
    message: str = "Authenticated"
    status: int = 200
