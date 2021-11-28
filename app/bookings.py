from producer import produce_entity, utopia_api_url, faker

from users import MIN_USER_PASSWORD_LEN, MAX_USER_PASSWORD_LEN
from flights import produce_flight

import random
import uuid

import bcrypt
import requests

PASSENGER_GENDER_OPTIONS = ["Male", "Female", "Non-binary", "Other"]

def produce_booking_agent(headers):
    response = requests.get(utopia_api_url + '/api/users', headers = headers)

    if response.status_code != 200:
        raise Exception("Unable to retrieve users", response.status_code)

    users = response.json()
    user = random.choice(users)
    while len(users) != 0 and user.role.name != "Agent":
        users.remove(user)
        user = random.choice(users)
    if user == None:
        response = requests.get(utopia_api_url + '/api/user-roles', headers = headers)

        if response.status_code != 200:
            raise Exception("Unable to retrieve user roles", response.status_code)

        user_roles = response.json()

        role = filter(lambda role: role.name == "Agent", user_roles)
        if len(role) == 0:
            raise Exception("Unable to find valid user role", 400)
        role = role[0]

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

    booking = produce_booking(headers).json()

    booking_agent = { 'booking': booking, 'agent': user }
    return produce_entity(
        '/api/booking-agents',
        headers,
        booking_agent,
        produce_booking_agent
    )

def produce_booking_user(headers):
    response = requests.get(utopia_api_url + '/api/users', headers = headers)

    if response.status_code != 200:
        raise Exception("Unable to retrieve users", response.status_code)

    users = response.json()
    user = random.choice(users)
    while len(users) != 0 and user.role.name != "User":
        users.remove(user)
        user = random.choice(users)
    if user == None:
        response = requests.get(utopia_api_url + '/api/user-roles', headers = headers)

        if response.status_code != 200:
            raise Exception("Unable to retrieve user roles", response.status_code)

        user_roles = response.json()

        role = filter(lambda role: role.name == "User", user_roles)
        if len(role) == 0:
            raise Exception("Unable to find valid user role", 400)
        role = role[0]

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

    booking = produce_booking(headers).json()

    booking_user = { 'booking': booking, 'user': user }
    return produce_entity(
        '/api/booking-users',
        headers,
        booking_user,
        produce_booking_user
    )

def produce_booking_guest(headers):
    booking = produce_booking(headers).json()

    booking_guest = { 'booking': booking, 'email': faker.email(), 'phone': faker.phone_number() }
    return produce_entity(
        '/api/booking-guests',
        headers,
        booking_guest,
        produce_booking_guest
    )

def produce_booking_payment(headers):
    response = requests.get(utopia_api_url + '/api/bookings', headers = headers)

    if response.status_code != 200:
        raise Exception("Unable to retrieve bookings", response.status_code)

    bookings = response.json()

    booking = random.choice(bookings)
    if booking == None:
        booking = produce_booking(headers).json()
    booking_payment = { 'booking': booking, 'stripe_id': faker.credit_card_full() }
    return produce_entity(
        '/api/booking-payments',
        headers,
        booking_payment,
        produce_booking_payment
    )

def produce_flight_booking(headers):
    response = requests.get(utopia_api_url + '/api/bookings', headers = headers)

    if response.status_code != 200:
        raise Exception("Unable to retrieve bookings", response.status_code)

    bookings = response.json()

    booking = random.choice(bookings)
    if booking == None:
        booking = produce_booking(headers).json()

    response = requests.get(utopia_api_url + '/api/flights', headers = headers)

    if response.status_code != 200:
        raise Exception("Unable to retrieve flights", response.status_code)

    flights = response.json()

    flight = random.choice(flights)
    if flight == None:
        flight = produce_flight(headers).json()

    flight_booking = { 'booking': booking, 'flight': flight }
    return produce_entity(
        '/api/flight-bookings',
        headers,
        flight_booking,
        produce_flight_booking
    )

def produce_booking(headers):
    booking = { 'confirmationCode': str(uuid.uuid1()) }
    return produce_entity(
        '/api/bookings',
        headers,
        booking,
        produce_booking
    )

def produce_passenger(headers):
    response = requests.get(utopia_api_url + '/api/bookings', headers = headers)

    if response.status_code != 200:
        raise Exception("Unable to retrieve bookings", response.status_code)

    bookings = response.json()

    booking = random.choice(bookings)
    if len(bookings) == 0:
        booking = produce_booking(headers).json()

    gender = random.choice(PASSENGER_GENDER_OPTIONS)

    passengere = {
        "booking": booking,
        "givenName": faker.first_name(),
        "familyName": faker.last_name(),
        "dateOfBirth": faker.birthdate(),
        "gender": gender,
        "address": faker.address()
    }

    return produce_entity(
        '/api/passengers',
        headers,
        passenger,
        produce_passenger
    )

