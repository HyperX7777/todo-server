from fastapi.testclient import TestClient
from sqlmodel import Field, Session, SQLModel, create_engine, select
from app.main import todo_server
from app import settings


# Important Links
# https://fastapi.tiangolo.com/tutorial/testing/
# https://sqlmodel.tiangolo.com/tutorial/fastapi/tests/#override-a-dependency
# https://realpython.com/python-assert-statement/
# https://understandingdata.com/posts/list-of-python-assert-statements-for-unit-tests/

client = TestClient(app=todo_server)


def test_welcome():
    greet: str = "Hey"
    assert greet == "Hey"


def test_fastapi_greetings():
    response = client.get("/")
    assert response.json() == {"Greetings: ": "HyperX"}


def test_create_todo():

    connection_string = str(settings.TEST_DATABASE_URL).replace(
        "postgresql", "postgresql+psycopg"
    )

    engine = create_engine(
        connection_string, connect_args={"sslmode": "require"}, pool_recycle=300
    )

    SQLModel.metadata.drop_all(engine)  # Drop all tables
    SQLModel.metadata.create_all(engine)  # Create tables

    with Session(engine) as session:

        def get_session_override():
            return session

        todo_server.dependency_overrides[Session] = get_session_override

        client = TestClient(app=todo_server)

        todo_id = "0"
        todo_title = "Testing"

        response = client.post("/todo", json={"id": todo_id, "title": todo_title})

        data = response.json()

        assert response.status_code == 200
        assert data["title"] == todo_title


def test_get_all_todos():

    connection_string = str(settings.TEST_DATABASE_URL).replace(
        "postgresql", "postgresql+psycopg"
    )

    engine = create_engine(
        connection_string, connect_args={"sslmode": "require"}, pool_recycle=300
    )

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:

        def get_session_override():
            return session

        todo_server.dependency_overrides[session] = get_session_override
        client = TestClient(app=todo_server)

        response = client.get("/todo")
        assert response.status_code == 200
