from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from ..models import Base
from sqlalchemy.orm import sessionmaker 
from ..main import app
from ..routers.todos import get_db, get_current_user
from fastapi.testclient import TestClient
from fastapi import status
import pytest
from ..models import ToDos

SQLALCHEMY_DATABASE_URL = 'sqlite:///./testdb.db'


engine = create_engine(
  SQLALCHEMY_DATABASE_URL,
  connect_args={'check_same_thread': False},  
  poolclass=StaticPool,     
) 

#'check_same_thread': False => позволяет использовать соединение в нескольких потоках.

#StaticPool => Он не создает пул в привычном смысле (как очередь соединений), а вместо этого повторно использует одно и то же соединение при каждом обращении.


TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

#  ⤴️ создаёт таблицы в базе данных, используя метаданные всех моделей, унаследованных от Base

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def override_get_current_user():
    return {'username': 'tester', 'id': 1, 'user_role': 'admin'}
        
app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


client = TestClient(app)


@pytest.fixture
def test_db():
    todo1 = ToDos(
      title='Learn to code! ', 
      description='Need to learn everyday! ',
      priority=5,
      complete=False, 
      owner_id=1
      )
    
    db = TestingSessionLocal()
    db.add(todo1)
    db.commit()
    yield todo1
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos"))
        connection.commit()



def test_read_all_authenticated(test_db):
    response = client.get('/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{'complete': False, 'title': 'Learn to code! ', 
                                'description': 'Need to learn everyday! ', 'id': 1, 
                                'priority': 5, 'owner_id': 1}]
