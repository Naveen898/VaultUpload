from datetime import datetime, timedelta, timezone
import jwt
import os
import uuid


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
SHARE_SECRET = os.getenv("SHARE_TOKEN_SECRET", SECRET_KEY)

def generate_token(username):
    payload = {"username": username}
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

def validate_token(token):
    try:
        jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return True
    except jwt.InvalidTokenError:
        return False

def generate_share_token(share_id: str, expires_at: datetime):
    """Generate a JWT for shared file access including expiry (exp)."""
    payload = {
        "sid": share_id,
        "exp": int(expires_at.replace(tzinfo=timezone.utc).timestamp()),
        "jti": str(uuid.uuid4())
    }
    return jwt.encode(payload, SHARE_SECRET, algorithm="HS256")

def decode_share_token(token: str):
    return jwt.decode(token, SHARE_SECRET, algorithms=["HS256"]) 
    