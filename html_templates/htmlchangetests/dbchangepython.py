import requests

r = requests.get('https://pno3cwa2.student.cs.kuleuven.be/api/task/list').json()

print(r)