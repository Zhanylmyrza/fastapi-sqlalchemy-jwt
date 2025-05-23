from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from pydantic import BaseModel, Field
from ..models import ToDos
from ..database import SessionLocal
from .auth import get_current_user


router=APIRouter()


def get_db():
  db= SessionLocal()
  try:
    yield db
  finally:
    db.close()
    
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/")
async def read_all(user: user_dependency, db: db_dependency):
  if user is None:
    raise HTTPException(status_code=401, detail='Authentication Failed')
  
  return db.query(ToDos).filter(ToDos.owner_id == user.get('id')).all()



@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
  
  if user is None:
    raise HTTPException(status_code=401, detail='Authentication Failed')
  
  
  todo_model = db.query(ToDos).filter(ToDos.id == todo_id).filter(ToDos.owner_id == user.get('id')).first() 
  
   
  if todo_model is not None:
    return todo_model
  raise HTTPException(status_code=404, detail="ToDo not found.")



class ToDoRequest(BaseModel):
  title: str = Field(min_length=3)
  description: str = Field(min_length=3, max_length=100)
  priority: int = Field(gt=0, lt=6)
  complete: bool
  

@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency, db: db_dependency, todo_request: ToDoRequest):
  
  if user is None:
    raise HTTPException(status_code=401, detail='Authentication Failed')
  
  todo_model = ToDos(**todo_request.dict(), owner_id=user.get('id'))
  
  db.add(todo_model)
  db.commit()


@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)  
async def update_todo(user: user_dependency, db: db_dependency,
                      todo_request: ToDoRequest,
                      todo_id: int = Path(gt=0)):
  
  if user is None:
    raise HTTPException(status_code=401, detail='Authentication Failed')
  
  
  todo_model = db.query(ToDos).filter(ToDos.id == todo_id).filter(ToDos.owner_id == user.get('id')).first()
  if todo_model is None:
    raise HTTPException(status_code=404, detail='ToDo not found')
  
  todo_model.title = todo_request.title
  todo_model.description = todo_request.description
  todo_model.priority = todo_request.priority
  todo_model.complete = todo_request.complete
  
  
  db.add(todo_model)
  db.commit()
  
  
@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency, 
                      todo_id: int = Path(gt=0)):
  
  if user is None:
    raise HTTPException(status_code=401, detail='Authentication Failed')
  
  
  todo_model = db.query(ToDos).filter(ToDos.id == todo_id).filter(ToDos.owner_id == user.get('id')).first()
  
  if todo_model is None:
    raise HTTPException(status_code=404, detail='ToDo not found')
  db.query(ToDos).filter(ToDos.id == todo_id).filter(ToDos.owner_id == user.get('id')).delete()
    
  db.commit()