from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import Column, Integer, String, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from fastapi.middleware.cors import CORSMiddleware

# Инициализация базы данных SQLite
DATABASE_URL = "sqlite:///./todo.db"
Base = declarative_base()
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Модель базы данных
class ToDoItem(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)

# Создание базы данных
Base.metadata.create_all(bind=engine)

# Инициализация FastAPI
app = FastAPI()

# Зависимость для работы с сессиями базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Схемы данных (Pydantic)
from pydantic import BaseModel

class ToDoCreate(BaseModel):
    title: str
    description: str = None

class ToDoUpdate(BaseModel):
    title: str = None
    description: str = None
    completed: bool = None

class ToDoResponse(BaseModel):
    id: int
    title: str
    description: str = None
    completed: bool

    class Config:
        from_attributes = True

# CRUD-операции

@app.post("/todos/", response_model=ToDoResponse)
def create_todo(todo: ToDoCreate, db: Session = Depends(get_db)):
    new_todo = ToDoItem(title=todo.title, description=todo.description)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

@app.get("/todos/", response_model=list[ToDoResponse])
def get_todos(db: Session = Depends(get_db)):
    return db.query(ToDoItem).all()

@app.get("/todos/{todo_id}", response_model=ToDoResponse)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(ToDoItem).filter(ToDoItem.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Task not found")
    return todo

@app.put("/todos/{todo_id}", response_model=ToDoResponse)
def update_todo(todo_id: int, todo_data: ToDoUpdate, db: Session = Depends(get_db)):
    todo = db.query(ToDoItem).filter(ToDoItem.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Task not found")
    if todo_data.title is not None:
        todo.title = todo_data.title
    if todo_data.description is not None:
        todo.description = todo_data.description
    if todo_data.completed is not None:
        todo.completed = todo_data.completed
    db.commit()
    db.refresh(todo)
    return todo

@app.delete("/todos/{todo_id}", response_model=dict)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(ToDoItem).filter(ToDoItem.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(todo)
    db.commit()
    return {"message": "Task deleted successfully"}


# Добавьте CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # URL вашего фронтенда
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)