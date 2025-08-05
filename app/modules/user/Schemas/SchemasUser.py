from pydantic import BaseModel, EmailStr, Field, model_validator
from typing import Optional, List

class UserBase(BaseModel):
    name: str
    email: EmailStr

class RoleOut(BaseModel):
    id: int
    name: str
    
    model_config = {
        "from_attributes": True
    }

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=128)
    confirm_pass: str = Field(..., min_length=8, max_length=128)
    role_id: int = Field(..., description="ID del rol a asignar al usuario")

    @model_validator(mode="after")
    def passwords_match(self):
        if self.password != self.confirm_pass:
            raise ValueError('Passwords do not match')
        return self

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8, max_length=128)
    confirm_pass: Optional[str] = Field(None, min_length=8, max_length=128)
    role_id: Optional[int] = Field(None, description="ID del rol a asignar al usuario")

    @model_validator(mode="after")
    def passwords_update_match(self):
        if (self.password or self.confirm_pass):
            if not self.password or not self.confirm_pass:
                raise ValueError('Both password and confirm_pass are required to update password')
            if self.password != self.confirm_pass:
                raise ValueError('Passwords do not match')
        return self

class UserOut(UserBase):
    id: int
    roles: List[RoleOut] = []
    
    model_config = {
        "from_attributes": True
    }
