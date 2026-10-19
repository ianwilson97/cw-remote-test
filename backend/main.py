"""A tiny todo API: in-memory, so every restart starts empty."""
import threading

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="todo-api")


class TodoIn(BaseModel):
    title: str


class Todo(TodoIn):
    id: int
    done: bool = False


todos: dict[int, Todo] = {}
next_id = 1
# sync handlers run in a threadpool, so every read or write of the store takes this
todos_lock = threading.Lock()


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/todos")
def list_todos() -> list[Todo]:
    with todos_lock:
        return list(todos.values())


@app.get("/api/todos/count")
def count_todos() -> dict[str, int]:
    with todos_lock:
        total = len(todos)
        done = sum(todo.done for todo in todos.values())
        return {"total": total, "done": done, "remaining": total - done}


@app.post("/api/todos", status_code=201)
def create_todo(body: TodoIn) -> Todo:
    global next_id
    with todos_lock:
        todo = Todo(id=next_id, title=body.title)
        todos[todo.id] = todo
        next_id += 1
    return todo


@app.patch("/api/todos/{todo_id}/toggle")
def toggle_todo(todo_id: int) -> Todo:
    with todos_lock:
        todo = todos.get(todo_id)
        if todo is None:
            raise HTTPException(404, "todo not found")
        todo.done = not todo.done
        return todo


@app.delete("/api/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int) -> None:
    with todos_lock:
        if todos.pop(todo_id, None) is None:
            raise HTTPException(404, "todo not found")
