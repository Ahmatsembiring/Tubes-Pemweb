from .auth import auth_views
from .jobs import job_views
from .applications import application_views
from .profiles import profile_views

def includeme(config):
    config.include(auth_views)
    config.include(job_views)
    config.include(application_views)
    config.include(profile_views)
