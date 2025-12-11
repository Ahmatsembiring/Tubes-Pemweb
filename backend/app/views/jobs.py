from pyramid.view import view_config
from pyramid.httpexceptions import HTTPBadRequest, HTTPUnauthorized, HTTPForbidden, HTTPNotFound
from sqlalchemy.orm import joinedload
import json

from ..models import Job, Employer, User
from ..models.user import UserRole
from ..models.job import JobType
from ..utils.auth import require_auth, require_role
from ..utils.validators import Validators

def job_views(config):
    config.add_route('jobs_list', '/jobs')
    config.add_route('jobs_create', '/jobs')
    config.add_route('jobs_detail', '/jobs/{job_id}')
    config.add_route('jobs_update', '/jobs/{job_id}')
    config.add_route('jobs_delete', '/jobs/{job_id}')
    
    config.add_view(list_jobs, route_name='jobs_list', request_method='GET', renderer='json')
    config.add_view(create_job, route_name='jobs_create', request_method='POST', renderer='json')
    config.add_view(get_job_detail, route_name='jobs_detail', request_method='GET', renderer='json')
    config.add_view(update_job, route_name='jobs_update', request_method='PUT', renderer='json')
    config.add_view(delete_job, route_name='jobs_delete', request_method='DELETE', renderer='json')

@view_config(route_name='jobs_list', request_method='GET', renderer='json')
def list_jobs(request):
    """Get all jobs with search and filter"""
    try:
        dbsession = request.dbsession
        
        # Query parameters
        title = request.GET.get('title', '')
        location = request.GET.get('location', '')
        salary_min = request.GET.get('salary_min')
        salary_max = request.GET.get('salary_max')
        job_type = request.GET.get('job_type', '')
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('per_page', 10))
        
        query = dbsession.query(Job).filter_by(is_active=1)
        
        # Filters
        if title:
            query = query.filter(Job.title.ilike(f'%{title}%'))
        if location:
            query = query.filter(Job.location.ilike(f'%{location}%'))
        if salary_min:
            query = query.filter(Job.salary_min >= float(salary_min))
        if salary_max:
            query = query.filter(Job.salary_max <= float(salary_max))
        if job_type:
            query = query.filter_by(job_type=JobType[job_type.upper()])
        
        # Pagination
        total = query.count()
        jobs = query.offset((page - 1) * per_page).limit(per_page).all()
        
        return {
            'total': total,
            'page': page,
            'per_page': per_page,
            'jobs': [job_to_dict(job) for job in jobs]
        }
    
    except Exception as e:
        raise HTTPBadRequest(detail=str(e))

@require_auth
@require_role('employer')
def create_job(request):
    """Create new job posting (Employer only)"""
    try:
        data = json.loads(request.body)
    except:
        raise HTTPBadRequest(detail='Invalid JSON')
    
    # Validate job data
    errors = Validators.validate_job_data(data)
    if errors:
        raise HTTPBadRequest(detail=json.dumps(errors))
    
    try:
        dbsession = request.dbsession
        user = dbsession.query(User).filter_by(id=request.user_id).first()
        employer = dbsession.query(Employer).filter_by(user_id=user.id).first()
        
        job = Job(
            employer_id=employer.id,
            title=data['title'].strip(),
            description=data['description'].strip(),
            requirements=data.get('requirements', '').strip(),
            salary_min=data.get('salary_min'),
            salary_max=data.get('salary_max'),
            location=data['location'].strip(),
            job_type=JobType[data.get('job_type', 'FULL_TIME').upper()],
            is_active=1
        )
        
        dbsession.add(job)
        dbsession.commit()
        
        return {'message': 'Job created successfully', 'job': job_to_dict(job)}
    
    except Exception as e:
        dbsession.rollback()
        raise HTTPBadRequest(detail=str(e))

def get_job_detail(request):
    """Get single job detail"""
    try:
        job_id = int(request.matchdict['job_id'])
        dbsession = request.dbsession
        
        job = dbsession.query(Job).filter_by(id=job_id).first()
        if not job:
            raise HTTPNotFound(detail='Job not found')
        
        return job_to_dict(job)
    
    except HTTPNotFound:
        raise
    except Exception as e:
        raise HTTPBadRequest(detail=str(e))

@require_auth
@require_role('employer')
def update_job(request):
    """Update job posting (Employer only)"""
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
        
        # Check if user is the employer
        if job.employer.user_id != request.user_id:
            raise HTTPForbidden(detail='Not authorized to update this job')
        
        # Update fields
        if 'title' in data:
            job.title = data['title'].strip()
        if 'description' in data:
            job.description = data['description'].strip()
        if 'requirements' in data:
            job.requirements = data['requirements'].strip()
        if 'salary_min' in data:
            job.salary_min = data['salary_min']
        if 'salary_max' in data:
            job.salary_max = data['salary_max']
        if 'location' in data:
            job.location = data['location'].strip()
        if 'job_type' in data:
            job.job_type = JobType[data['job_type'].upper()]
        
        dbsession.commit()
        return {'message': 'Job updated successfully', 'job': job_to_dict(job)}
    
    except (HTTPNotFound, HTTPForbidden):
        raise
    except Exception as e:
        dbsession.rollback()
        raise HTTPBadRequest(detail=str(e))

@require_auth
@require_role('employer')
def delete_job(request):
    """Delete job posting (Employer only)"""
    try:
        job_id = int(request.matchdict['job_id'])
        dbsession = request.dbsession
        
        job = dbsession.query(Job).filter_by(id=job_id).first()
        
        if not job:
            raise HTTPNotFound(detail='Job not found')
        
        if job.employer.user_id != request.user_id:
            raise HTTPForbidden(detail='Not authorized to delete this job')
        
        dbsession.delete(job)
        dbsession.commit()
        
        return {'message': 'Job deleted successfully'}
    
    except (HTTPNotFound, HTTPForbidden):
        raise
    except Exception as e:
        dbsession.rollback()
        raise HTTPBadRequest(detail=str(e))

def job_to_dict(job):
    """Convert job object to dictionary"""
    return {
        'id': job.id,
        'title': job.title,
        'description': job.description,
        'requirements': job.requirements,
        'salary_min': job.salary_min,
        'salary_max': job.salary_max,
        'location': job.location,
        'job_type': job.job_type.value,
        'company_name': job.employer.company_name,
        'employer_id': job.employer_id,
        'is_active': job.is_active,
        'created_at': job.created_at.isoformat(),
        'updated_at': job.updated_at.isoformat()
    }
