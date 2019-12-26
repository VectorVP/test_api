import requests

# POST ID=1
def post1():
    url = "http://127.0.0.1:5000/api/user"
    payload = "{\n\t\"email\": \"ivan@mail.ru\",\n\t\"name\" : \"Иван\",\n\t\"language\": \"ru\"\n}\n"
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data = payload)
    print(response.text.encode('utf8'))

# POST ID=2
def post2():
    url = "http://127.0.0.1:5000/api/user"
    payload = "{\n\t\"email\": \"oleg@mail.ru\",\n\t\"name\" : \"Олег\",\n\t\"language\": \"eng\"\n}\n"
    headers = {
      'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data = payload)
    print(response.text.encode('utf8'))

# GET ID=2
def get_one():
    url = "http://127.0.0.1:5000/api/user/2"
    payload = {}
    headers= {}
    response = requests.request("GET", url, headers=headers, data = payload)
    print(response.text.encode('utf8'))

# GET ALL
def get_all():
    url = "http://127.0.0.1:5000/api/user"
    payload = {}
    headers= {}
    response = requests.request("GET", url, headers=headers, data = payload)
    print(response.text.encode('utf8'))

# UPDATE ID=2
def update2():
    url = "http://127.0.0.1:5000/api/user/2"

    payload = "{\n\t\"email\": \"oleg@mail.ru\",\n\t\"name\" : \"Сергей\",\n\t\"language\": \"eng\"\n}\n"
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("PUT", url, headers=headers, data = payload)
    print(response.text.encode('utf8'))

# DELETE ID=1
def delete1():
    url = "http://127.0.0.1:5000/api/user/1"
    payload = {}
    headers = {
    }
    response = requests.request("DELETE", url, headers=headers, data=payload)
    print(response.text.encode('utf8'))



