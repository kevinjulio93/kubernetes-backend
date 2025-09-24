from fastapi import FastAPI, Depends, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session
from .database import init_db, get_session
from . import crud, schemas

app = FastAPI(title="Tasks API")

# Allow local frontend during development
app.add_middleware(
    CORSMiddleware,
    # allow all origins in dev; do not allow credentials when using wildcard
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    # ensure models are imported so SQLModel metadata is populated
    from . import models  # noqa: F401
    init_db()


@app.post("/tasks", response_model=schemas.TaskRead)
def create_task(task_in: schemas.TaskCreate, session: Session = Depends(get_session)):
    return crud.create_task(session, task_in)


@app.get("/tasks", response_model=list[schemas.TaskRead])
def read_tasks(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    return crud.list_tasks(session, skip, limit)


@app.get("/tasks/{task_id}", response_model=schemas.TaskRead)
def read_task(task_id: int, session: Session = Depends(get_session)):
    task = crud.get_task(session, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.put("/tasks/{task_id}", response_model=schemas.TaskRead)
def update_task(task_id: int, task_in: schemas.TaskUpdate, session: Session = Depends(get_session)):
    task = crud.update_task(session, task_id, task_in)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, session: Session = Depends(get_session)):
    ok = crud.delete_task(session, task_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"deleted": True}


# Development helper: respond to preflight explicitly for JS clients
@app.options("/tasks")
def options_tasks():
    return Response(status_code=200)


@app.options("/tasks/{task_id}")
def options_task_id(task_id: int):
    return Response(status_code=200)
