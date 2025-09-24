from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TaskCreate(BaseModel):
    name: str
    exec_time_seconds: int = 0
    status: Optional[str] = "pending"
    notes: Optional[str] = None


class TaskRead(TaskCreate):
    id: int
    created_at: datetime
    updated_at: datetime


class TaskUpdate(BaseModel):
    name: Optional[str] = None
    exec_time_seconds: Optional[int] = None
    status: Optional[str] = None
    notes: Optional[str] = None
