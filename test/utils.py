from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker 
from ..models import Base
from ..main import app
from fastapi.testclient import TestClient
import pytest
from ..models import ToDos, User
from ..routers.auth import bcrypt_context




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
        
        
                
client = TestClient(app)

@pytest.fixture
def test_todos():
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


@pytest.fixture
def test_users():
  user1 = User(
    username='codingwithme',
    email ='codingwithme@gmail.com',
    first_name='Coding',
    last_name='WithMe',
    hashed_password=bcrypt_context.hash('test_password'),
    role='admin',
    phone_number='123 - 456 - 789'
  )
  db = TestingSessionLocal()
  db.add(user1)
  db.commit()
  yield user1
  with engine.connect() as connection:
    connection.execute(text("DELETE FROM users"))
    connection.commit()