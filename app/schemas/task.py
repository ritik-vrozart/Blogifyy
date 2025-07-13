

from pydantic import BaseModel

class CreateTask(BaseModel):
    title: str
    description: str
    user_id: str
    completed: bool = False

class UpdateTask(BaseModel):
    title: str
    description: str