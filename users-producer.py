#!/bin/python3
import os, requests, random
from faker import Faker
import bcrypt

def produce_user():
    role = random.choice([
        { "id": 1, "name": "Employee" },
        { "id": 2, "name": "Traveller" },
        { "id": 3, "name": "Admin" }
    ])
    password = bcrypt.hashpw(faker.password(length=16).encode('utf-8'), bcrypt.gensalt())
    return {
        "role": role,
        "givenName": faker.first_name(),
        "familyName": faker.last_name(),
        "username": faker.user_name(),
        "email": faker.email(),
        "password": str(password, encoding = 'utf-8'),
        "phone": faker.phone_number(),
    }

if __name__ == '__main__':
    faker = Faker('en_US')
    api_host = 'http://' + os.environ['USERS_API_HOST']

    # First, login as an Admin
    token = requests.post(api_host + '/login', json = { 'username': 'awalter', 'password': 'password' })
    headers = { "Authorization": "Bearer {}".format(token.json()["token"]) }
    print(headers)
    # Then use this token for producing users
    user = produce_user()
    print(user)
    print(requests.post(api_host + '/api/users', headers = headers, json = user).json())
