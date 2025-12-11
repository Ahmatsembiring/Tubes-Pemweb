from pyramid.config import Configurator
from sqlalchemy.orm import scoped_session, sessionmaker
from app.config import DatabaseConfig
from app.models import Base
import json
from pyramid.httpexceptions import HTTPException

def main(global_config, **settings):
    """Pyramid application factory"""
    
    # Setup database
    engine = DatabaseConfig.get_engine(settings)
    session_factory = scoped_session(sessionmaker(bind=engine))
    
    # Create all tables
    Base.metadata.create_all(engine)
    
    # Create Pyramid configuration
    config = Configurator(settings=settings)
    
    # Add database session to each request
    def add_dbsession(event):
        request = event.request
        request.dbsession = session_factory()
        
        def cleanup(request):
            session_factory.remove()
        
        request.add_finished_callback(cleanup)
    
    config.add_subscriber(add_dbsession, 'pyramid.events.NewRequest')
    
    # Add error handler
    def error_handler(exc, request):
        """Handle errors and return JSON"""
        response = request.response
        response.content_type = 'application/json'
        
        if isinstance(exc, HTTPException):
            response.status = exc.status
            error_detail = exc.detail if exc.detail else str(exc)
        else:
            response.status = 500
            error_detail = str(exc)
        
        response.body = json.dumps({'error': error_detail}).encode('utf-8')
        return response
    
    config.add_view(error_handler, context=Exception, renderer='json')
    
    # CORS middleware
    def cors_factory(handler, registry):
        def cors_handler(request):
            response = handler(request)
            response.headers.update({
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST,GET,OPTIONS,PUT,DELETE,PATCH',
                'Access-Control-Allow-Headers': 'Content-Type,Authorization',
                'Access-Control-Max-Age': '3600'
            })
            return response
        return cors_handler
    
    config.add_tween('app.cors_factory')
    
    # Include view configuration
    config.include('app.views')
    
    return config.make_wsgi_app()
