from sqlmodel import create_engine, SQLModel, Session
from pathlib import Path

# DB file in backend directory
DB_PATH = Path(__file__).resolve().parents[1] / "tasks.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
