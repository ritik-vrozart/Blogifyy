from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.models.user import Task, User
from app.schemas.task import CreateTask

task_api = APIRouter()


@task_api.post("/create")
async def create_task(request:CreateTask,db:Session = Depends(get_db)):
    new_task = Task(title=request.title, description=request.description, user_id=request.user_id, completed=request.completed)
    db.add(new_task)
    db.commit()
    return {"message": "Task created successfully"}

@task_api.get("/get")
async def get_task(db:Session = Depends(get_db), search: str = Query(None, description="Search tasks by title")):
    # Base query with join
    query = db.query(Task, User).join(User, Task.user_id == User.id)
    
    # Add search filter if provided
    if search:
        query = query.filter(Task.title.ilike(f"%{search}%"))
    
    tasks_with_users = query.all()
    
    # Convert tasks to array format with user details
    task_array = []
    for task, user in tasks_with_users:
        task_dict = {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "user_id": task.user_id,
            "completed": task.completed,
            "created_at": task.created_at if hasattr(task, 'created_at') else None,
            "updated_at": task.updated_at if hasattr(task, 'updated_at') else None,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "created_at": user.created_at if hasattr(user, 'created_at') else None
            }
        }
        task_array.append(task_dict)
    
    return {"tasks": task_array}

