from datetime import datetime, timedelta
import jwt
#from flask import current_app
import os


'''class JWTService:
    def __init__(self):
        self.secret_key = current_app.config['JWT_SECRET_KEY']
        self.algorithm = 'HS256'

    def generate_token(self, user_id, expires_in=3600):
        expiration = datetime.utcnow() + timedelta(seconds=expires_in)
        token = jwt.encode({'user_id': user_id, 'exp': expiration}, self.secret_key, algorithm=self.algorithm)
        return token

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload['user_id']
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    def is_token_valid(self, token):
        return self.decode_token(token) is not None
'''
SECRET_KEY = os.getenv("JWT_SECRET", "your_local_secret")

def generate_token(username):
    # Example payload
    payload = {"username": username}
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

def validate_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return True
    except jwt.InvalidTokenError:
        return False