import requests

def produce_entity(url, headers, entity, produce_function):
    response = requests.post(url = url, headers = headers, json = entity)

    if response.status_code / 100 == 5:
        raise Exception("Users API microservice experienced internal error", response.status_code)

    if response.status_code != 200:
        response = produce_function(headers)

    return response
