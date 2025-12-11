from pyramid.view import view_config
from pyramid.httpexceptions import HTTPBadRequest, HTTPNotFound, HTTPForbidden
import json

from ..models import User, JobSeeker, Employer
from ..models.user import UserRole
from ..utils.auth import require_auth, require_role

def profile_views(config):
    config.add_route('profile_get', '/profile')
    config.add_route('profile_update', '/profile')
    config.add_route('profile_get_employer', '/employers/{employer_id}')
    
    config.add_view(get_profile, route_name='profile_get', request_method='GET', renderer='json')
    config.add_view(update_profile, route_name='profile_update', request_method='PUT', renderer='json')
    config.add_view(get_employer_profile, route_name='profile_get_employer', request_method='GET', renderer='json')

@require_auth
def get_profile(request):
    """Get current user profile"""
    try:
        dbsession = request.dbsession
        user = dbsession.query(User).filter_by(id=request.user_id).first()
        
        if not user:
            raise HTTPNotFound(detail='User not found')
        
        if user.role == UserRole.JOB_SEEKER:
            profile = dbsession.query(JobSeeker).filter_by(user_id=user.id).first()
            return {
                'user': user_to_dict(user),
                'profile': job_seeker_to_dict(profile)
            }
        else:
            profile = dbsession.query(Employer).filter_by(user_id=user.id).first()
            return {
                'user': user_to_dict(user),
                'profile': employer_to_dict(profile)
            }
    
    except Exception as e:
        raise HTTPBadRequest(detail=str(e))

@require_auth
def update_profile(request):
    """Update current user profile"""
    try:
        data = json.loads(request.body)
    except:
        raise HTTPBadRequest(detail='Invalid JSON')
    
    try:
        dbsession = request.dbsession
        user = dbsession.query(User).filter_by(id=request.user_id).first()
        
        if not user:
            raise HTTPNotFound(detail='User not found')
        
        # Update user fields
        if 'full_name' in data:
            full_name = data['full_name'].strip()
            if len(full_name) < 2:
                raise HTTPBadRequest(detail='Full name must be at least 2 characters')
            user.full_name = full_name
        
        # Update role-specific profile
        if user.role == UserRole.JOB_SEEKER:
            profile = dbsession.query(JobSeeker).filter_by(user_id=user.id).first()
            if 'skills' in data:
                profile.skills = data['skills']
            if 'experience_years' in data:
                profile.experience_years = int(data['experience_years'])
            if 'phone' in data:
                profile.phone = data['phone']
            if 'location' in data:
                profile.location = data['location'].strip()
            if 'bio' in data:
                profile.bio = data['bio'].strip()
            if 'cv_url' in data:
                profile.cv_url = data['cv_url']
        else:
            profile = dbsession.query(Employer).filter_by(user_id=user.id).first()
            if 'company_name' in data:
                company_name = data['company_name'].strip()
                if len(company_name) < 2:
                    raise HTTPBadRequest(detail='Company name must be at least 2 characters')
                profile.company_name = company_name
            if 'company_description' in data:
                profile.company_description = data['company_description'].strip()
            if 'company_logo_url' in data:
                profile.company_logo_url = data['company_logo_url']
            if 'company_website' in data:
                profile.company_website = data['company_website'].strip()
            if 'phone' in data:
                profile.phone = data['phone']
            if 'location' in data:
                profile.location = data['location'].strip()
        
        dbsession.commit()
        
        return {
            'message': 'Profile updated successfully',
            'user': user_to_dict(user),
            'profile': job_seeker_to_dict(profile) if user.role == UserRole.JOB_SEEKER else employer_to_dict(profile)
        }
    
    except HTTPBadRequest:
        raise
    except Exception as e:
        dbsession.rollback()
        raise HTTPBadRequest(detail=str(e))

def get_employer_profile(request):
    """Get employer public profile"""
    try:
        employer_id = int(request.matchdict['employer_id'])
        dbsession = request.dbsession
        
        employer = dbsession.query(Employer).filter_by(id=employer_id).first()
        if not employer:
            raise HTTPNotFound(detail='Employer not found')
        
        return {
            'employer': employer_to_dict(employer),
            'user': user_to_dict(employer.user)
        }
    
    except HTTPNotFound:
        raise
    except Exception as e:
        raise HTTPBadRequest(detail=str(e))

def user_to_dict(user):
    """Convert user to dictionary"""
    return {
        'id': user.id,
        'email': user.email,
        'full_name': user.full_name,
        'role': user.role.value,
        'is_email_verified': user.is_email_verified,
        'created_at': user.created_at.isoformat()
    }

def job_seeker_to_dict(profile):
    """Convert job seeker profile to dictionary"""
    return {
        'id': profile.id,
        'user_id': profile.user_id,
        'skills': profile.skills,
        'experience_years': profile.experience_years,
        'cv_url': profile.cv_url,
        'phone': profile.phone,
        'location': profile.location,
        'bio': profile.bio,
        'created_at': profile.created_at.isoformat()
    }

def employer_to_dict(profile):
    """Convert employer profile to dictionary"""
    return {
        'id': profile.id,
        'user_id': profile.user_id,
        'company_name': profile.company_name,
        'company_description': profile.company_description,
        'company_logo_url': profile.company_logo_url,
        'company_website': profile.company_website,
        'phone': profile.phone,
        'location': profile.location,
        'created_at': profile.created_at.isoformat()
    }
