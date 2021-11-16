import producer

import os, random

import requests
from faker import Faker

MIN_AIRPLANE_CAPACITY = 40
MAX_AIRPLANE_CAPACITY = 80

flights_api_url = os.getenv('FLIGHTS_API_URL')
faker = Faker('en_US')

def produce_airport(headers):
    # Assumes city has more than 3 alphabetical chars
    def alpha_chars(str):
        return ''.join(filter(lambda c: c.isalpha(), str))
    city = faker.city()
    code = ''
    code += random.choice(alpha_chars(city[:-2]))
    code += random.choice(alpha_chars(city[city.find(code[0]):-1]))
    code += random.choice(alpha_chars(city[city.find(code[1]):]))
    airport = { 'code': code.upper(), 'city': city }

    return producer.produce_entity(flights_api_url + '/api/airports', headers, airport, produce_airport)


def produce_airplane_type(headers):
    airplane_type = { "maxCapacity":  random.randint(MIN_AIRPLANE_CAPACITY, MAX_AIRPLANE_CAPACITY) }

    return producer.produce_entity(flights_api_url + '/api/airplane-types', headers, airplane_type, produce_airplane_type)

