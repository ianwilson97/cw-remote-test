import pytest
from fastapi.testclient import TestClient

import main


@pytest.fixture(autouse=True)
def fresh():
    main.todos.clear()
    main.next_id = 1


client = TestClient(main.app)


def test_health():
    assert client.get("/api/health").json() == {"status": "ok"}


def test_create_list_toggle_delete():
    created = client.post("/api/todos", json={"title": "write tests"})
    assert created.status_code == 201
    assert created.json() == {"id": 1, "title": "write tests", "done": False}
    assert client.get("/api/todos").json() == [created.json()]
    assert client.patch("/api/todos/1/toggle").json()["done"] is True
    assert client.delete("/api/todos/1").status_code == 204
    assert client.get("/api/todos").json() == []


def test_missing_todo_is_404():
    assert client.patch("/api/todos/99/toggle").status_code == 404
    assert client.delete("/api/todos/99").status_code == 404
