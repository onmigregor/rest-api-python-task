from pydantic import BaseModel, EmailStr, Field
from typing import Optional

from pydantic import model_validator

class UserCreateRequest(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    confirm_pass: str = Field(..., min_length=8, max_length=128)

    @model_validator(mode="after")
    def passwords_match(self):
        if self.password != self.confirm_pass:
            raise ValueError('Passwords do not match')
        return self

class UserUpdateRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=100)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8, max_length=128)
    confirm_pass: Optional[str] = Field(None, min_length=8, max_length=128)

    @model_validator(mode="after")
    def passwords_update_match(self):
        if (self.password or self.confirm_pass):
            if not self.password or not self.confirm_pass:
                raise ValueError('Both password and confirm_pass are required to update password')
            if self.password != self.confirm_pass:
                raise ValueError('Passwords do not match')
        return self

class UserOutResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    class Config:
        from_attributes = True

class SuccessResponse(BaseModel):
    message: str = "success"
    data: object

class NotFoundResponse(BaseModel):
    message: str = "Not found"
    status: int = 404
