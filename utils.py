import validators
import random
import string

def randomShortString(length):
    return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(length))

def isValidUrl(value):
    return validators.url(value)
