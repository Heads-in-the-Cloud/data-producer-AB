from producer import produce_entity, utopia_api_url, faker

import random

import bcrypt
import requests

MIN_USER_ROLE_NUM = 0
MAX_USER_ROLE_NUM = 255
MIN_USER_PASSWORD_LEN = 16
MAX_USER_PASSWORD_LEN = 255

def produce_user_role(headers):
    name = { 'name': 'Role {}'.format(random.randint(MIN_USER_ROLE_NUM, MAX_USER_ROLE_NUM)) }

    return produce_entity('/api/user-roles', headers, name, produce_user_role)

def produce_user(headers):
    response = requests.get(utopia_api_url + '/api/user-roles', headers = headers)

    if response.status_code != 200:
        raise Exception("Unable to retrieve user roles", response.status_code)

    user_roles = response.json()

    role = random.choice(user_roles)
    if len(user_roles) == 0:
        raise Exception("No user roles available to choose from", 400)

    password_len = random.randint(MIN_USER_PASSWORD_LEN, MAX_USER_PASSWORD_LEN)
    password = bcrypt.hashpw(faker.password(length = password_len), bcrypt.gensalt())

    user = {
        "role": role,
        "givenName": faker.first_name(),
        "familyName": faker.last_name(),
        "username": faker.user_name(),
        "email": faker.email(),
        "password": password,
        "phone": faker.phone_number()
    }

    return produce_entity('/api/users', headers, user, produce_user)
