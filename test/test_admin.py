from .utils import *
from ..routers.admin import get_db, get_current_user
from fastapi import status
from ..models import ToDos

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_admin_read_all_authenticated(test_todos):
  response = client.get("/admin/todos")
  assert response.status_code == status.HTTP_200_OK
  assert response.json() == [ {'complete': False, 'title': 'Learn to code! ', 
                                'description': 'Need to learn everyday! ', 'id': 1, 
                                'priority': 5, 'owner_id': 1} ]
  
  
def test_admin_delete_any_todos(test_todos):
  response = client.delete("/admin/todo/1")
  assert response.status_code == status.HTTP_204_NO_CONTENT
  
  db = TestingSessionLocal()
  model = db.query(ToDos).filter(ToDos.id == 1).first()
  assert model is None
  

def test_admin_delete_todo_not_found():
  response = client.delete("/admin/todo/293746")
  assert response.status_code == status.HTTP_404_NOT_FOUND
  assert response.json() == {'detail': 'ToDo not found'}