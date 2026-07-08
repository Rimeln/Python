from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

app = FastAPI(
    title="To-Do API",
    description="Простой REST API для управления задачами",
    version="1.0.0",
)

# --- Модели данных ---

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    done: Optional[bool] = None

class Task(BaseModel):
    id: int
    title: str
    description: Optional[str]
    done: bool
    created_at: str

# --- "База данных" в памяти ---

tasks: dict[int, Task] = {}
next_id = 1

# --- Маршруты ---

@app.get("/", tags=["Общее"])
def root():
    return {"message": "Добро пожаловать в To-Do API 🚀"}


@app.get("/tasks", response_model=list[Task], tags=["Задачи"])
def get_tasks():
    """Получить все задачи."""
    return list(tasks.values())


@app.get("/tasks/{task_id}", response_model=Task, tags=["Задачи"])
def get_task(task_id: int):
    """Получить задачу по ID."""
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return tasks[task_id]


@app.post("/tasks", response_model=Task, status_code=201, tags=["Задачи"])
def create_task(body: TaskCreate):
    """Создать новую задачу."""
    global next_id
    task = Task(
        id=next_id,
        title=body.title,
        description=body.description,
        done=False,
        created_at=datetime.now().isoformat(),
    )
    tasks[next_id] = task
    next_id += 1
    return task


@app.patch("/tasks/{task_id}", response_model=Task, tags=["Задачи"])
def update_task(task_id: int, body: TaskUpdate):
    """Обновить задачу (частично)."""
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    task = tasks[task_id]
    updated = task.model_dump()
    if body.title is not None:
        updated["title"] = body.title
    if body.description is not None:
        updated["description"] = body.description
    if body.done is not None:
        updated["done"] = body.done
    tasks[task_id] = Task(**updated)
    return tasks[task_id]


@app.delete("/tasks/{task_id}", tags=["Задачи"])
def delete_task(task_id: int):
    """Удалить задачу."""
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    del tasks[task_id]
    return {"message": f"Задача {task_id} удалена"}
