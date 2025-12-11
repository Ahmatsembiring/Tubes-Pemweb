from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from sqlalchemy.orm import scoped_session
import json

from app.config import DatabaseConfig
from app.models import Base
from app import views

def main(global_config, **settings):
    """Main Pyramid app factory"""
    
    # Database setup
    engine = DatabaseConfig.get_engine(settings)
    session_factory = DatabaseConfig.get_session(engine)
    
    # Create tables
    Base.metadata.create_all(engine)
    
    config = Configurator(settings=settings)
    
    # Add database session to request
    def add_dbsession(event):
        request = event.request
        request.dbsession = session_factory()
        
        def cleanup(request):
            request.dbsession.close()
        
        request.add_finished_callback(cleanup)
    
    config.add_subscriber(add_dbsession, 'pyramid.events.NewRequest')
    
    # CORS middleware
    def cors_middleware(request):
        response = request.invoke_subrequest(request.wrapped_request, use_exception_response=True)
        response.headers.update({
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST,GET,OPTIONS,PUT,DELETE',
            'Access-Control-Allow-Headers': 'Content-Type,Authorization'
        })
        return response
    
    config.add_tween('main.cors_middleware')
    
    # Include views
    config.include(views)
    
    # Error handlers
    config.add_view(error_handler, context=Exception, renderer='json')
    
    return config.make_wsgi_app()

def error_handler(exc, request):
    """Handle exceptions and return JSON response"""
    response = request.response
    
    if hasattr(exc, 'detail'):
        response.status = exc.status or 400
        response.body = json.dumps({'error': exc.detail}).encode('utf-8')
    else:
        response.status = 500
        response.body = json.dumps({'error': 'Internal server error'}).encode('utf-8')
    
    response.content_type = 'application/json'
    return response

if __name__ == '__main__':
    from pyramid.scripts.pserve import setup_logging
    
    settings = {
        'db_user': 'postgres',
        'db_password': 'password',
        'db_host': 'localhost',
        'db_port': '5432',
        'db_name': 'job_portal_db',
        'db_echo': False,
        'pyramid.reload_templates': True,
        'pyramid.debug_authorization': True,
        'pyramid.debug_notfound': True,
        'pyramid.debug_routematch': True,
        'jwt_secret_key': 'your-secret-key-change-in-production',
        'frontend_url': 'http://localhost:3000'
    }
    
    app = main({}, **settings)
    server = make_server('0.0.0.0', 6543, app)
    print('Server started on http://localhost:6543')
    server.serve_forever()
