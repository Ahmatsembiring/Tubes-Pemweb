from pyramid.view import view_config
from pyramid.httpexceptions import HTTPBadRequest, HTTPConflict, HTTPUnauthorized
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import json
from datetime import datetime

from ..models import User, JobSeeker, Employer
from ..models.user import UserRole
from ..utils.auth import AuthManager
from ..utils.validators import Validators
from ..utils.password import PasswordManager
from ..utils.email import EmailService

def auth_views(config):
    config.add_route('auth_register', '/auth/register')
    config.add_route('auth_login', '/auth/login')
    config.add_route('auth_verify_email', '/auth/verify-email')
    config.add_view(register, route_name='auth_register', request_method='POST', renderer='json')
    config.add_view(login, route_name='auth_login', request_method='POST', renderer='json')
    config.add_view(verify_email, route_name='auth_verify_email', request_method='POST', renderer='json')

@view_config(route_name='auth_register', request_method='POST', renderer='json')
def register(request):
    """Register new user (Job Seeker or Employer)"""
    try:
        data = json.loads(request.body)
    except:
        raise HTTPBadRequest(detail='Invalid JSON')
    
    role = data.get('role', '').lower()
    if role not in ['job_seeker', 'employer']:
        raise HTTPBadRequest(detail='Invalid role. Must be job_seeker or employer')
    
    # Validate input
    errors = Validators.validate_registration_data(data, role)
    if errors:
        raise HTTPBadRequest(detail=json.dumps(errors))
    
    email = data['email'].strip()
    password = data['password']
    full_name = data['full_name'].strip()
    
    try:
        dbsession = request.dbsession
        
        # Check if email already exists
        existing_user = dbsession.query(User).filter_by(email=email).first()
        if existing_user:
            raise HTTPConflict(detail='Email already registered')
        
        # Create user
        password_hash = PasswordManager.hash_password(password)
        verification_token = EmailService.generate_verification_token()
        
        user = User(
            email=email,
            password_hash=password_hash,
            full_name=full_name,
            role=UserRole.EMPLOYER if role == 'employer' else UserRole.JOB_SEEKER,
            email_verification_token=verification_token,
            is_email_verified=False
        )
        
        dbsession.add(user)
        dbsession.flush()  # Get user ID
        
        # Create profile based on role
        if role == 'employer':
            company_name = data.get('company_name', '').strip()
            employer = Employer(
                user_id=user.id,
                company_name=company_name
            )
            dbsession.add(employer)
        else:
            job_seeker = JobSeeker(user_id=user.id)
            dbsession.add(job_seeker)
        
        dbsession.commit()
        
        # Send verification email
        frontend_url = request.registry.settings.get('frontend_url', 'http://localhost:3000')
        EmailService.send_verification_email(email, verification_token, frontend_url)
        
        return {
            'message': 'Registration successful. Please check your email to verify.',
            'user_id': user.id,
            'email': user.email,
            'role': role
        }
    
    except IntegrityError:
        dbsession.rollback()
        raise HTTPConflict(detail='Email already registered')
    except Exception as e:
        dbsession.rollback()
        raise HTTPBadRequest(detail=str(e))

@view_config(route_name='auth_login', request_method='POST', renderer='json')
def login(request):
    """Login user and return JWT token"""
    try:
        data = json.loads(request.body)
    except:
        raise HTTPBadRequest(detail='Invalid JSON')
    
    email = data.get('email', '').strip()
    password = data.get('password', '')
    
    if not email or not password:
        raise HTTPBadRequest(detail='Email and password required')
    
    try:
        dbsession = request.dbsession
        user = dbsession.query(User).filter_by(email=email).first()
        
        if not user or not PasswordManager.verify_password(password, user.password_hash):
            raise HTTPUnauthorized(detail='Invalid email or password')
        
        if not user.is_email_verified:
            raise HTTPUnauthorized(detail='Please verify your email first')
        
        # Generate token
        token = AuthManager.generate_token(user.id, user.role.value)
        
        return {
            'message': 'Login successful',
            'token': token,
            'user': {
                'id': user.id,
                'email': user.email,
                'full_name': user.full_name,
                'role': user.role.value
            }
        }
    
    except HTTPUnauthorized:
        raise
    except Exception as e:
        raise HTTPBadRequest(detail=str(e))

@view_config(route_name='auth_verify_email', request_method='POST', renderer='json')
def verify_email(request):
    """Verify email using token"""
    try:
        data = json.loads(request.body)
    except:
        raise HTTPBadRequest(detail='Invalid JSON')
    
    token = data.get('token', '').strip()
    if not token:
        raise HTTPBadRequest(detail='Verification token required')
    
    try:
        dbsession = request.dbsession
        user = dbsession.query(User).filter_by(email_verification_token=token).first()
        
        if not user:
            raise HTTPBadRequest(detail='Invalid verification token')
        
        user.is_email_verified = True
        user.email_verification_token = None
        dbsession.commit()
        
        return {'message': 'Email verified successfully'}
    
    except Exception as e:
        dbsession.rollback()
        raise HTTPBadRequest(detail=str(e))
