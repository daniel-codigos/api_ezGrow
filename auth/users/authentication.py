import jwt, datetime
from rest_framework import exceptions
#from ..auth.settings import SECRET_KEY

SECRET_KEY = 'django-insecure-i9fd%0z8_-97-t@!^(mihs7(dvq_mm&k3*-(-10cx-srurcq9*'

def create_access_token(id,email):
    return jwt.encode({
        'user_id': id,
        'email':email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=55),
        'iat': datetime.datetime.utcnow()
    }, SECRET_KEY,algorithm='HS256')


def decode_access_token(token):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms='HS256')

        return payload['user_id'],payload['email']
    except:
        raise exceptions.AuthenticationFailed('Desautentificado!! jiji')

def create_refresh_token(id,email):
    return jwt.encode({
        'user_id': id,
        'email':email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
        'iat': datetime.datetime.utcnow()
    }, SECRET_KEY,algorithm='HS256')


def decode_refresh_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms='HS256')

        return payload['user_id'],payload['email']
    except:
        raise exceptions.AuthenticationFailed('Desautentificado!! jeje')