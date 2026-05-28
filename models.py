from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    role = Column(String) # 'teacher' or 'student'
    is_active = Column(Boolean, default=True)

class Classroom(Base):
    __tablename__ = "classrooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    subject = Column(String)
    room = Column(String)
    teacher_id = Column(Integer, ForeignKey("users.id"))
    
    teacher = relationship("User")

class BroadcastMessage(Base):
    __tablename__ = "broadcasts"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    teacher_id = Column(Integer, ForeignKey("users.id"))
    
    teacher = relationship("User")

class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"))
    classroom_id = Column(Integer, ForeignKey("classrooms.id"))
    date = Column(DateTime, default=datetime.utcnow)
    status = Column(String) # 'present', 'absent', 'late'
    
    student = relationship("User")
    classroom = relationship("Classroom")
