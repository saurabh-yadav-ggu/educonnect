from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class UserBase(BaseModel):
    email: str
    full_name: str
    role: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    email: str
    password: str

class ClassroomBase(BaseModel):
    name: str
    subject: str
    room: str

class ClassroomCreate(ClassroomBase):
    pass

class ClassroomResponse(ClassroomBase):
    id: int
    teacher_id: int

    class Config:
        from_attributes = True

class BroadcastBase(BaseModel):
    content: str

class BroadcastCreate(BroadcastBase):
    pass

class BroadcastResponse(BroadcastBase):
    id: int
    created_at: datetime
    teacher_id: int

    class Config:
        from_attributes = True

class AttendanceBase(BaseModel):
    status: str
    classroom_id: int

class AttendanceCreate(AttendanceBase):
    student_id: int

class AttendanceResponse(AttendanceBase):
    id: int
    student_id: int
    date: datetime

    class Config:
        from_attributes = True
