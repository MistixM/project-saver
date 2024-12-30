import string
import random

def generate_token(length=24):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))