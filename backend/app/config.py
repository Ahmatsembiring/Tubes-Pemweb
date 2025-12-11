import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

class DatabaseConfig:
    """Database configuration"""
    
    @staticmethod
    def get_engine(settings):
        """Create SQLAlchemy engine"""
        db_user = settings.get('db_user', 'postgres')
        db_password = settings.get('db_password', 'password')
        db_host = settings.get('db_host', 'localhost')
        db_port = settings.get('db_port', '5432')
        db_name = settings.get('db_name', 'job_portal_db')
        
        connection_string = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
        
        engine = create_engine(
            connection_string,
            echo=settings.get('db_echo', False),
            pool_size=20,
            max_overflow=40
        )
        return engine
    
    @staticmethod
    def get_session(engine):
        """Create scoped session"""
        session_factory = sessionmaker(bind=engine)
        return scoped_session(session_factory)
