from pyramid.view import view_config
from pyramid.httpexceptions import HTTPBadRequest, HTTPUnauthorized, HTTPForbidden, HTTPNotFound
from sqlalchemy.orm import joinedload
import json

from ..models import Application, Job, JobSeeker, Employer, User
from ..models.user import UserRole
from ..models.application import ApplicationStatus
from ..utils.auth import require_auth, require_role
from ..utils.validators import Validators

def application_views(config):
    config.add_route('applications_list', '/applications')
    config.add_route('applications_create', '/jobs/{job_id}/apply')
    config.add_route('applications_detail', '/applications/{app_id}')
    config.add_route('applications_update', '/applications/{app_id}')
    
    config.add_view(list_applications, route_name='applications_list', request_method='GET', renderer='json')
    config.add_view(create_application, route_name='applications_create', request_method='POST', renderer='json')
    config.add_view(get_application, route_name='applications_detail', request_method='GET', renderer='json')
    config.add_view(update_application, route_name='applications_update', request_method='PUT', renderer='json')

@require_auth
def list_applications(request):
    """
    Get applications:
    - Employer: all applications for their jobs
    - Job Seeker: only their applications
    """
    try:
        dbsession = request.dbsession
        user = dbsession.query(User).filter_by(id=request.user_id).first()
        
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('per_page', 10))
        status = request.GET.get('status')
        
        query = dbsession.query(Application)
        
        if user.role.value == 'employer':
            # Get employer's job IDs
            employer = dbsession.query(Employer).filter_by(user_id=user.id).first()
            job_ids = [job.id for job in employer.jobs]
            query = query.filter(Application.job_id.in_(job_ids))
        else:
            # Get job seeker's applications
            job_seeker = dbsession.query(JobSeeker).filter_by(user_id=user.id).first()
            query = query.filter_by(job_seeker_id=job_seeker.id)
        
        if status:
            query = query.filter_by(status=ApplicationStatus[status.upper()])
        
        total = query.count()
        applications = query.offset((page - 1) * per_page).limit(per_page).all()
        
        return {
            'total': total,
            'page': page,
            'per_page': per_page,
            'applications': [app_to_dict(app) for app in applications]
        }
    
    except Exception as e:
        raise HTTPBadRequest(detail=str(e))

@require_auth
@require_role('job_seeker')
def create_application(request):
    """Job Seeker applies for a job"""
    try:
        data = json.loads(request.body)
        job_id = int(request.matchdict['job_id'])
    except:
        raise HTTPBadRequest(detail='Invalid JSON or job_id')
    
    try:
        dbsession = request.dbsession
        
        job = dbsession.query(Job).filter_by(id=job_id).first()
        if not job:
            raise HTTPNotFound(detail='Job not found')
        
        job_seeker = dbsession.query(JobSeeker).filter_by(user_id=request.user_id).first()
        
        # Check if already applied
        existing = dbsession.query(Application).filter_by(
            job_id=job_id,
            job_seeker_id=job_seeker.id
        ).first()
        
        if existing:
            raise HTTPBadRequest(detail='Already applied for this job')
        
        application = Application(
            job_id=job_id,
            job_seeker_id=job_seeker.id,
            cover_letter=data.get('cover_letter', '').strip(),
            status=ApplicationStatus.APPLIED
        )
        
        dbsession.add(application)
        dbsession.commit()
        
        return {
            'message': 'Application submitted successfully',
            'application': app_to_dict(application)
        }
    
    except (HTTPNotFound, HTTPBadRequest):
        raise
    except Exception as e:
        dbsession.rollback()
        raise HTTPBadRequest(detail=str(e))

def get_application(request):
    """Get application detail"""
    try:
        app_id = int(request.matchdict['app_id'])
        dbsession = request.dbsession
        
        application = dbsession.query(Application).filter_by(id=app_id).first()
        if not application:
            raise HTTPNotFound(detail='Application not found')
        
        return app_to_dict(application)
    
    except HTTPNotFound:
        raise
    except Exception as e:
        raise HTTPBadRequest(detail=str(e))

@require_auth
@require_role('employer')
def update_application(request):
    """
    Employer updates application status:
    - reviewed
    - shortlisted
    - rejected
    - accepted
    """
    try:
        data = json.loads(request.body)
        app_id = int(request.matchdict['app_id'])
    except:
        raise HTTPBadRequest(detail='Invalid JSON or app_id')
    
    status = data.get('status', '').upper()
    valid_statuses = ['REVIEWED', 'SHORTLISTED', 'REJECTED', 'ACCEPTED']
    
    if status not in valid_statuses:
        raise HTTPBadRequest(detail=f'Invalid status. Must be one of: {", ".join(valid_statuses)}')
    
    try:
        dbsession = request.dbsession
        application = dbsession.query(Application).filter_by(id=app_id).first()
        
        if not application:
            raise HTTPNotFound(detail='Application not found')
        
        # Check if user is the employer of the job
        if application.job.employer.user_id != request.user_id:
            raise HTTPForbidden(detail='Not authorized to update this application')
        
        application.status = ApplicationStatus[status]
        application.notes = data.get('notes', '')
        
        dbsession.commit()
        
        return {
            'message': 'Application updated successfully',
            'application': app_to_dict(application)
        }
    
    except (HTTPNotFound, HTTPForbidden):
        raise
    except Exception as e:
        dbsession.rollback()
        raise HTTPBadRequest(detail=str(e))

def app_to_dict(application):
    """Convert application object to dictionary"""
    return {
        'id': application.id,
        'job_id': application.job_id,
        'job_title': application.job.title,
        'job_seeker_id': application.job_seeker_id,
        'seeker_name': application.job_seeker.user.full_name,
        'seeker_email': application.job_seeker.user.email,
        'status': application.status.value,
        'cover_letter': application.cover_letter,
        'notes': application.notes,
        'applied_at': application.applied_at.isoformat(),
        'updated_at': application.updated_at.isoformat()
    }
