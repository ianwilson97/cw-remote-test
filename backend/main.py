"""A tiny todo API: in-memory, so every restart starts empty."""
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


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/todos")
def list_todos() -> list[Todo]:
    return list(todos.values())


@app.get("/api/todos/count")
def count_todos() -> dict[str, int]:
    done = sum(todo.done for todo in todos.values())
    return {"total": len(todos), "done": done, "remaining": len(todos) - done}


@app.post("/api/todos", status_code=201)
def create_todo(body: TodoIn) -> Todo:
    global next_id
    todo = Todo(id=next_id, title=body.title)
    todos[todo.id] = todo
    next_id += 1
    return todo


@app.patch("/api/todos/{todo_id}/toggle")
def toggle_todo(todo_id: int) -> Todo:
    todo = todos.get(todo_id)
    if todo is None:
        raise HTTPException(404, "todo not found")
    todo.done = not todo.done
    return todo


@app.delete("/api/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int) -> None:
    if todos.pop(todo_id, None) is None:
        raise HTTPException(404, "todo not found")
