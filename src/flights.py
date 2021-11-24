from producer import produce_entity, utopia_api_url, faker

import random

import requests

MIN_AIRPLANE_CAPACITY = 40
MAX_AIRPLANE_CAPACITY = 80
MIN_FLIGHT_DEPARTURE_TIME = 'now'
MAX_FLIGHT_DEPARTURE_TIME = '+2y'
MIN_FLIGHT_SEAT_PRICE = 120.0
MAX_FLIGHT_SEAT_PRICE = 300.50

def produce_airport(headers): # Assumes city has more than 3 alphabetical chars
    def alpha_chars(str):
        return ''.join(filter(lambda c: c.isalpha(), str))
    city = faker.city()
    code = ''
    code += random.choice(alpha_chars(city[:-2]))
    code += random.choice(alpha_chars(city[city.find(code[0]):-1]))
    code += random.choice(alpha_chars(city[city.find(code[1]):]))
    airport = { 'code': code.upper(), 'city': city }

    return produce_entity('/api/airports', headers, airport, produce_airport)

def produce_airplane(headers):
    response = requests.get(utopia_api_url + '/api/airplane-types', headers = headers)

    if response.status_code != 200:
        raise Exception("Unable to retrieve airplane types", response.status_code)

    airplane_types = response.json()

    type = random.choice(airplane_types)
    if len(airplane_types) == 0:
        type = produce_airplane_type(headers).json()

    airplane = { "type": type }

    return produce_entity('/api/airplanes', headers, airplane, produce_airplane)

def produce_airplane_type(headers):
    airplane_type = { "maxCapacity":  random.randint(MIN_AIRPLANE_CAPACITY, MAX_AIRPLANE_CAPACITY) }

    return produce_entity('/api/airplane-types', headers, airplane_type, produce_airplane_type)

def produce_flight(headers):
    response = requests.get(utopia_api_url + '/api/routes', headers = headers)

    if response.status_code != 200:
        raise Exception("Unable to retrieve routes", response.status_code)

    routes = response.json()

    route = random.choice(routes)
    if len(routes) == 0:
        route = produce_route(headers)

    response = requests.get(utopia_api_url + '/api/airplanes', headers = headers)

    if response.status_code != 200:
        raise Exception("Unable to retrieve airplanes", response.status_code)

    airplanes = response.json()

    airplane = random.choice(airplanes)
    if len(airplanes) == 0:
        airplane = produce_airplane(headers)

    time_of_departure = faker.date_time_between(start_date = MIN_FLIGHT_DEPARTURE_TIME, end_date = MAX_FLIGHT_DEPARTURE_TIME).isoformat(sep='T', timespec='milliseconds')

    seat_price = round(random.uniform(MIN_FLIGHT_SEAT_PRICE, MAX_FLIGHT_SEAT_PRICE), 2)

    flight = {
        'route': route,
        'airplane': airplane,
        'timeOfDeparture': str(time_of_departure) + '+00:00',
        'reservedSeats': 0,
        'seatPrice': seat_price
    }
    return produce_entity('/api/flights', headers, flight, produce_flight)


def produce_route(headers):
    response = requests.get(utopia_api_url + '/api/airports', headers = headers)

    if response.status_code != 200:
        raise Exception("Unable to retrieve airports", response.status_code)

    airports = response.json()

    if len(airports) < 2:
        airports.append(produce_airport(headers).json())
    if len(airports) == 1:
        airports.append(produce_airport(headers).json())
    origin = random.choice(airports)
    airports.remove(origin)
    dest = random.choice(airports)

    route = { "origin": origin, "destination": dest }

    return produce_entity('/api/routes', headers, route, produce_route)

