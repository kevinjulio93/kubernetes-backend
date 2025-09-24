from sqlmodel import Session, select
from .models import Task
from .schemas import TaskCreate, TaskUpdate
from datetime import datetime


def create_task(session: Session, task_in: TaskCreate) -> Task:
    task = Task.from_orm(task_in)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def get_task(session: Session, task_id: int):
    return session.get(Task, task_id)


def list_tasks(session: Session, skip: int = 0, limit: int = 100):
    statement = select(Task).offset(skip).limit(limit)
    return session.exec(statement).all()


def update_task(session: Session, task_id: int, task_in: TaskUpdate):
    task = session.get(Task, task_id)
    if not task:
        return None
    for key, value in task_in.dict(exclude_unset=True).items():
        setattr(task, key, value)
    task.updated_at = datetime.utcnow()
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def delete_task(session: Session, task_id: int):
    task = session.get(Task, task_id)
    if not task:
        return False
    session.delete(task)
    session.commit()
    return True
