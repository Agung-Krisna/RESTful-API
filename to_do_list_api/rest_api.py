from fastapi import FastAPI, Form
from fastapi.encoders import jsonable_encoder
from tortoise_database import dbInit
from tortoise_models import ToDo
from tortoise.contrib.fastapi import register_tortoise
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise import run_async

# create connection with database
dbInit()

# initialize the app
app = FastAPI()

# using tortoise inside our api
register_tortoise(
    app,
    db_url = "sqlite://./todo.db",
    modules = {"models": ["tortoise_models"]},
    generate_schemas=True,
    add_exception_handlers=True
)

# serialize object into JSON using pydantic
todo_pydantic = pydantic_model_creator(ToDo)

# serialize object into JSON without id (no readonly value)
todo_pydantic_without_id = pydantic_model_creator(ToDo, exclude_readonly=True)

@app.get("/")
async def home():
    return {"message": "an API for a To Do List"}

@app.get("/list_todos")
async def get_list():
    return await todo_pydantic.from_queryset(ToDo.all())

@app.get("/todo/{todo_id}")
async def get_todo(todo_id: int):
    return await todo_pydantic_without_id.from_queryset_single(ToDo.get(id=todo_id))
@app.post("/todo/new/")
async def post_todo(title=Form(...), description=Form(...)):
    todo = await ToDo.create(title=title, description=description)
    return await todo_pydantic.from_tortoise_orm(todo)

@app.put("/todo/{todo_id}", response_model=todo_pydantic)
async def update_todo(todo_id: int, todo_object: todo_pydantic_without_id):
    await ToDo.filter(id=todo_id).update(**todo_object.dict())
    return await todo_pydantic_without_id.from_queryset_single(ToDo.get(id=todo_id))

@app.delete("/todo/{todo_id}")
async def delete_todo(todo_id: int):
    await ToDo.filter(id=todo_id).delete()
    return {"deletion_id": todo_id}