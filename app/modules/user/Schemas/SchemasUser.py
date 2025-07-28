from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    name: str
    email: EmailStr

from pydantic import model_validator, Field

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=128)
    confirm_pass: str = Field(..., min_length=8, max_length=128)

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
    model_config = {
        "from_attributes": True
    }
