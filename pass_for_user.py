import random


def generate_password():
    password_length = 5
    password = ''.join(random.choices('0123456789', k=password_length))
    return password



