from requests import delete
print(delete('http://localhost:5000/api/threads/3', json={'user_id': 1, 'password': 'admin'}).json())
