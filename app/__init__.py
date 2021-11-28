#!/bin/python3

import bookings
import flights
import users
from producer import utopia_api_url

from concurrent.futures import ThreadPoolExecutor

import requests
from flask import Flask, request, json, jsonify

app = Flask(__name__)

def produce_entities(total, produce_function):
    login_path = '{}/api/login'.format(utopia_api_url)
    
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

@app.errorhandler(Exception)
def server_error(e):
    """Return JSON instead of HTML for HTTP errors."""
    if len(e.args) == 0:
        # start with the correct headers and status code from the error
        response = e.get_response()
        # replace the body with JSON
        response.data = json.dumps({
            "code": e.code,
            "name": e.name,
            "description": e.description,
        })
        response.content_type = "application/json"
        return response
    return jsonify({ 'message': e.args[0] }), 500

@app.route('/user-roles/<int:total>', methods = [ 'POST' ])
def user_roles_endpoint(total):
    return { 'user-roles': produce_entities(total, users.produce_user_role) }, 201

@app.route('/users/<int:total>', methods = [ 'POST' ])
def users_endpoint(total):
    return { 'users': produce_entities(total, users.produce_user) }, 201

@app.route('/airports/<int:total>', methods = [ 'POST' ])
def airports_endpoint(total):
    return { 'airports': produce_entities(total, flights.produce_airport) }, 201

@app.route('/airplanes/<int:total>', methods = [ 'POST' ])
def airplanes_endpoint(total):
    return { 'airplanes': produce_entities(total, flights.produce_airplane) }, 201

@app.route('/airplane-types/<int:total>', methods = [ 'POST' ])
def airplane_types_endpoint(total):
    return { 'airplane-types': produce_entities(total, flights.produce_airplane_type) }, 201

@app.route('/flights/<int:total>', methods = [ 'POST' ])
def flights_endpoint(total):
    return { 'flights': produce_entities(total, flights.produce_flight) }, 201

@app.route('/routes/<int:total>', methods = [ 'POST' ])
def routes_endpoint(total):
    return { 'routes': produce_entities(total, flights.produce_route) }, 201

@app.route('/bookings/<int:total>', methods = [ 'POST' ])
def bookings_endpoint(total):
    return { 'bookings': produce_entities(total, bookings.produce_booking) }, 201

@app.route('/booking-agents/<int:total>', methods = [ 'POST' ])
def booking_agents_endpoint(total):
    return { 'booking-agents': produce_entities(total, bookings.produce_booking_agent) }, 201

@app.route('/booking-users/<int:total>', methods = [ 'POST' ])
def booking_users_endpoint(total):
    return { 'bookings-users': produce_entities(total, bookings.produce_booking_user) }, 201

@app.route('/bookings-guests/<int:total>', methods = [ 'POST' ])
def bookings_guests_endpoint(total):
    return { 'booking-guests': produce_entities(total, bookings.produce_booking_guest) }, 201

@app.route('/booking-payments/<int:total>', methods = [ 'POST' ])
def booking_payments_endpoint(total):
    return { 'bookings-payments': produce_entities(total, bookings.produce_booking_payment) }, 201

@app.route('/flight-bookings/<int:total>', methods = [ 'POST' ])
def flight_bookings_endpoint(total):
    return { 'flight-bookings': produce_entities(total, bookings.produce_flight_booking) }, 201

@app.route('/passengers/<int:total>', methods = [ 'POST' ])
def passengers_endpoint(total):
    return { 'passengers': produce_entities(total, bookings.produce_passenger) }, 201

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000)
