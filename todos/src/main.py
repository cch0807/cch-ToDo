from typing import List
from fastapi import Depends, FastAPI, Body, HTTPException
from sqlalchemy.orm import Session

from todos.src.database.connection import get_db
from todos.src.database.orm import ToDo
from todos.src.database.repository import (
    create_todo,
    delete_todo,
    get_todo_by_id,
    get_todos,
    update_todo,
)
from todos.src.schema.request import CreateToDoRequest
from todos.src.schema.response import ToDoListSchema, ToDoSchema

app = FastAPI()


@app.get("/")
def health_check_handler():
    return {"ping": "pong"}


todo_data = {
    1: {"id": 1, "content": "test data 1", "is_done": True},
    2: {"id": 2, "content": "test data 2", "is_done": False},
    3: {"id": 3, "content": "test data 3", "is_done": False},
}


@app.get("/todos", status_code=200)
def get_todos_handler(
    order: str | None = None, session: Session = Depends(get_db)
) -> ToDoListSchema:
    todos: List[ToDo] = get_todos(session=session)

    if order and order == "DESC":
        return ToDoListSchema(todos=[ToDoSchema.from_orm(todo) for todo in todos][::-1])
    return ToDoListSchema(todos=[ToDoSchema.from_orm(todo) for todo in todos])


@app.get("/todos/{todo_id}", status_code=200)
def get_todo_handler(todo_id: int, session: Session = Depends(get_db)) -> ToDoSchema:
    todo: ToDo | None = get_todo_by_id(session=session, todo_id=todo_id)
    if todo:
        return ToDoSchema.from_orm(todo)
    raise HTTPException(status_code=404, detail="ToDo Not Found")


@app.post("/todos", status_code=201)
def create_todo_handler(request: CreateToDoRequest, session: Session = Depends(get_db)):
    todo: ToDo = ToDo.create(request=request)  # id = None
    todo: ToDo = create_todo(session=session, todo=todo)  # id = int

    return ToDoSchema.from_orm(todo)


@app.patch("/todos/{todo_id}", status_code=200)
def update_todo_handler(
    todo_id: int,
    is_done: bool = Body(..., embed=True),
    session: Session = Depends(get_db),
):
    todo: ToDo | None = get_todo_by_id(session=session, todo_id=todo_id)
    if todo:
        # update
        todo.done() if is_done else todo.undone()
        todo: ToDo = update_todo(session=session, todo=todo)
        return ToDoSchema.from_orm(todo)
    raise HTTPException(status_code=404, detail="ToDo Not Found")


@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo_handler(todo_id: int, session: Session = Depends(get_db)):
    todo: ToDo | None = get_todo_by_id(session=session, todo_id=todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="ToDo Not Found")
    delete_todo(session=session, todo_id=todo_id)
