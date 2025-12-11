import jwt
import os
from datetime import datetime, timedelta
from functools import wraps
from pyramid.request import Request
from pyramid.httpexceptions import HTTPUnauthorized, HTTPForbidden

class AuthManager:
    SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'your-secret-key-change-in-production')
    ALGORITHM = 'HS256'
    ACCESS_TOKEN_EXPIRE_HOURS = 24
    
    @staticmethod
    def generate_token(user_id: int, role: str) -> str:
        """Generate JWT token"""
        payload = {
            'user_id': user_id,
            'role': role,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(hours=AuthManager.ACCESS_TOKEN_EXPIRE_HOURS)
        }
        token = jwt.encode(payload, AuthManager.SECRET_KEY, algorithm=AuthManager.ALGORITHM)
        return token
    
    @staticmethod
    def verify_token(token: str) -> dict:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, AuthManager.SECRET_KEY, algorithms=[AuthManager.ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPUnauthorized(detail='Token has expired')
        except jwt.InvalidTokenError:
            raise HTTPUnauthorized(detail='Invalid token')
    
    @staticmethod
    def get_token_from_header(request: Request) -> str:
        """Extract token from Authorization header"""
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            raise HTTPUnauthorized(detail='Missing or invalid authorization header')
        return auth_header[7:]  # Remove 'Bearer ' prefix

def require_auth(func):
    """Decorator untuk protect endpoints yang perlu authentication"""
    @wraps(func)
    def wrapper(request: Request, *args, **kwargs):
        try:
            token = AuthManager.get_token_from_header(request)
            payload = AuthManager.verify_token(token)
            request.user_id = payload['user_id']
            request.user_role = payload['role']
        except HTTPUnauthorized:
            raise
        return func(request, *args, **kwargs)
    return wrapper

def require_role(*roles):
    """Decorator untuk check role-based access"""
    def decorator(func):
        @wraps(func)
        def wrapper(request: Request, *args, **kwargs):
            if not hasattr(request, 'user_role'):
                raise HTTPUnauthorized(detail='Authentication required')
            if request.user_role not in roles:
                raise HTTPForbidden(detail='Insufficient permissions')
            return func(request, *args, **kwargs)
        return wrapper
    return decorator
