import requests
import os
from faker import Faker

faker = Faker('en_US')
utopia_api_url = os.getenv('UTOPIA_API_URL')

def produce_entity(path_route, headers, entity, produce_function):
    response = requests.post(url = utopia_api_url + path_route, headers = headers, json = entity)

    if response.status_code / 100 == 5:
        raise Exception("Users API microservice experienced internal error", response.status_code)

    #if response.status_code != 200:
    #    response = produce_function(headers)

    return response
