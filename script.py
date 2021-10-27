#!/bin/python3
import os, requests, random
from faker import Faker

def produce_airport():
    while True:
        city = faker.city()
        if len(city) >= 3:
            break
    code = ''
    code += random.choice(city[:-2])
    code += random.choice(city[city.find(code[0]):-1])
    code += random.choice(city[city.find(code[1]):])
    return { 'code': code.upper(), 'city': city }

if __name__ == '__main__':
    faker = Faker('en_US')
    api_host = 'http://' + os.environ['API_HOST']

    airport = None
    while True:
        airport = produce_airport()
        response = requests.get(api_host + '/airport/' + airport['code'])
        if response.status_code == 404:
            break
    requests.post(api_host + '/airport', json = airport)
