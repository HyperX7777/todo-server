from fastapi import FastAPI, Depends
from typing import Annotated
from sqlmodel import SQLModel, Field, create_engine, Session, select
from app import settings
from contextlib import asynccontextmanager

# --- Step 1: Database Table SCHEMA


class Todo(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str


# --- Step 2: Connection to the Database

connection_string: str = str(settings.DATABASE_URL).replace(
    "postgresql", "postgresql+psycopg"
)

engine = create_engine(connection_string)


def create_db_tables():
    print("Creating Tables")
    SQLModel.metadata.create_all(engine)
    print("Done")


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Server Starting")
    create_db_tables()
    yield


# --- Step 3: Table Data Save or Get

todo_server: FastAPI = FastAPI(lifespan=lifespan)


def get_session():
    with Session(engine) as session:
        yield session


@todo_server.get("/")
def greetings_user():
    return {"Greetings: ": "HyperX"}


@todo_server.post("/todo")
def create_todo(todo_data: Todo, session: Annotated[Session, Depends(get_session)]):
    #   with Session(engine) as session:
    session.add(todo_data)
    session.commit()
    session.refresh(todo_data)
    return todo_data


# --- Get all ToDo's Data


@todo_server.get("/todo")
def get_all_todos(new_concept: Annotated[Session, Depends(get_session)]):
    #   with Session(engine) as session :
    query = select(Todo)
    #   session = Session(engine)
    # --- Select All Todos
    get_all_todos = new_concept.exec(query).all()
    #   session.close()
    return get_all_todos
