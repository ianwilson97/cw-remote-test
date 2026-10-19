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


def test_count_of_empty_list():
    assert client.get("/api/todos/count").json() == {"total": 0, "done": 0, "remaining": 0}


def test_count_after_creating_and_toggling():
    for title in ("a", "b", "c"):
        client.post("/api/todos", json={"title": title})
    client.patch("/api/todos/2/toggle")
    assert client.get("/api/todos/count").json() == {"total": 3, "done": 1, "remaining": 2}
    client.patch("/api/todos/2/toggle")
    assert client.get("/api/todos/count").json() == {"total": 3, "done": 0, "remaining": 3}
    client.delete("/api/todos/1")
    assert client.get("/api/todos/count").json() == {"total": 2, "done": 0, "remaining": 2}


def test_count_is_not_shadowed_by_todo_id_routes():
    client.post("/api/todos", json={"title": "only"})
    counted = client.get("/api/todos/count")
    assert counted.status_code == 200
    assert counted.json() == {"total": 1, "done": 0, "remaining": 1}
    # the paths that do take a todo id still treat "count" as an int path param
    assert client.delete("/api/todos/count").status_code == 422
    assert client.get("/api/todos/count").status_code == 200
