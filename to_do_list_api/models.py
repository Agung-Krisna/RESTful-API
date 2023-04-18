from pydantic import BaseModel
from db.database import Database
from typing import Optional

class ToDoList(BaseModel):
    title: str
    description: Optinoal[str]
    is_completed: bool = False

