from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
from database import get_db

router = APIRouter()

@router.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    # Note: In production, hash the password!
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password, full_name=user.full_name, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/classrooms/", response_model=List[schemas.ClassroomResponse])
def read_classrooms(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    classrooms = db.query(models.Classroom).offset(skip).limit(limit).all()
    return classrooms

@router.post("/classrooms/", response_model=schemas.ClassroomResponse)
def create_classroom(classroom: schemas.ClassroomCreate, teacher_id: int, db: Session = Depends(get_db)):
    db_classroom = models.Classroom(**classroom.dict(), teacher_id=teacher_id)
    db.add(db_classroom)
    db.commit()
    db.refresh(db_classroom)
    return db_classroom

@router.post("/broadcasts/", response_model=schemas.BroadcastResponse)
def create_broadcast(broadcast: schemas.BroadcastCreate, teacher_id: int, db: Session = Depends(get_db)):
    db_broadcast = models.BroadcastMessage(**broadcast.dict(), teacher_id=teacher_id)
    db.add(db_broadcast)
    db.commit()
    db.refresh(db_broadcast)
    return db_broadcast

@router.get("/broadcasts/", response_model=List[schemas.BroadcastResponse])
def get_broadcasts(db: Session = Depends(get_db)):
    return db.query(models.BroadcastMessage).order_by(models.BroadcastMessage.created_at.desc()).all()

@router.post("/auth/login", response_model=schemas.UserResponse)
def login(request: schemas.LoginRequest, db: Session = Depends(get_db)):
    # This is a mock login - in a real app you'd use OAuth2PasswordRequestForm and verify hashes
    db_user = db.query(models.User).filter(models.User.email == request.email).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return db_user

@router.post("/attendance/", response_model=schemas.AttendanceResponse)
def mark_attendance(attendance: schemas.AttendanceCreate, db: Session = Depends(get_db)):
    db_attendance = models.Attendance(**attendance.dict())
    db.add(db_attendance)
    db.commit()
    db.refresh(db_attendance)
    return db_attendance
