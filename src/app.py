#!/bin/python3

import bookings
import flights
import users

from concurrent.futures import ThreadPoolExecutor
import os

import requests
from flask import Flask, request

app = Flask(__name__)

users_api_url = os.getenv('USERS_API_URL')

def produce_entities(total, produce_function):
    login_path = '{}/api/login'.format(users_api_url)
    
    response = requests.post(url = login_path, params = request.authorization)

    if response.status_code / 100 == 5:
        raise Exception("Users API microservice experienced internal error", response.status_code)

    if response.status_code != 200:
        raise Exception("Unable to login", response.status_code)

    headers = { "Authorization": "Bearer {}".format(response.json()['access_token']) } 

    results = []
    with ThreadPoolExecutor() as executor:
        for _ in range(total):
            results.append(executor.submit(produce_function, (headers)))
    return list(map(lambda future: future.result().json(), results))

@app.route('/user-roles/<int:total>', methods = [ 'POST' ])
def user_roles_endpoint(total):
    return { 'user-roles': produce_entities(total, users.produce_user_role) }

@app.route('/users/<int:total>', methods = [ 'POST' ])
def users_endpoint(total):
    return { 'users': produce_entities(total, users.produce_user) }

@app.route('/airports/<int:total>', methods = [ 'POST' ])
def airports_endpoint(total):
    return { 'airports': produce_entities(total, flights.produce_airport) }

#@app.route('/airplanes/<int:total>', methods = [ 'POST' ])
#def airplanes(total):
#    return { 'airplanes': produce_entities(total, flights.produce_airplane) }

@app.route('/airplane-types/<int:total>', methods = [ 'POST' ])
def airplane_types(total):
    return { 'airplane-types': produce_entities(total, flights.produce_airplane_type) }

#@app.route('/flights/<int:total>', methods = [ 'POST' ])
#def flights(total):
#    return { 'flights': produce_entities(total, flights.produce_flight) }
#
#@app.route('/routes/<int:total>', methods = [ 'POST' ])
#def routes(total):
#    return { 'routes': produce_entities(total, flights.produce_route) }
#
#@app.route('/bookings/<int:total>', methods = [ 'POST' ])
#def bookings(total):
#    return { 'bookings': produce_entities(total, bookings.produce_booking) }
#
#@app.route('/booking-agents/<int:total>', methods = [ 'POST' ])
#def booking_agents(total):
#    return { 'booking-agents': produce_entities(total, bookings.produce_booking_agent) }
#
#@app.route('/booking-users/<int:total>', methods = [ 'POST' ])
#def booking_users(total):
#    return { 'bookings-users': produce_entities(total, bookings.produce_booking_user) }
#
#@app.route('/bookings-guests/<int:total>', methods = [ 'POST' ])
#def bookings_guests(total):
#    return { 'booking-guests': produce_entities(total, bookings.produce_booking_guest) }
#
#@app.route('/booking-payments/<int:total>', methods = [ 'POST' ])
#def booking_payments(total):
#    return { 'bookings-payments': produce_entities(total, bookings.produce_booking_payment) }
#
#@app.route('/flight-bookings/<int:total>', methods = [ 'POST' ])
#def flight_bookings(total):
#    return { 'flight-bookings': produce_entities(total, bookings.produce_flight_booking) }
#
#@app.route('/passengers/<int:total>', methods = [ 'POST' ])
#def passengers(total):
#    return { 'passengers': produce_entities(total, bookings.produce_passenger) }

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000)
