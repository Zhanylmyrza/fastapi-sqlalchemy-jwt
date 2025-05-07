from .utils import *
from ..routers.users import get_db, get_current_user
from fastapi import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_return_all_users(test_users):
    response = client.get('/users')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == 'codingwithme'
    assert response.json()['email'] == 'codingwithme@gmail.com'
    assert response.json()['first_name'] == 'Coding'
    assert response.json()['last_name'] == 'WithMe'
    assert response.json()['phone_number'] == '123 - 456 - 789'
    assert response.json()['role'] == 'admin'
    
    
def test_change_password(test_users):
  
  request = client.put('/users/password', json={'password': 'test_password',
                                                'new_password': 'new_password'})
  assert request.status_code == status.HTTP_204_NO_CONTENT
  
  
def test_change_password_invalid_current_password(test_users):
  
  request = client.put('/users/password', json={'password': 'wrong_password',
                                                'new_password': 'new_password'})
  assert request.status_code == status.HTTP_401_UNAUTHORIZED
  assert request.json() == {'detail': 'Error on password change'}
  
  
def test_change_phone_number(test_users):
  
  request = client.put('/users/phone/222222222', json={'phone_number': '987 - 654 - 321'})
  assert request.status_code == status.HTTP_204_NO_CONTENT  
