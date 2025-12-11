"""WSGI entry point untuk production deployment"""
import os
from pyramid.paster import get_app
from dotenv import load_dotenv

load_dotenv()

# Baca configuration dari environment
settings = {
    'db_user': os.getenv('DB_USER', 'postgres'),
    'db_password': os.getenv('DB_PASSWORD', 'password'),
    'db_host': os.getenv('DB_HOST', 'localhost'),
    'db_port': os.getenv('DB_PORT', '5432'),
    'db_name': os.getenv('DB_NAME', 'job_portal_db'),
    'db_echo': os.getenv('DB_ECHO', 'false').lower() == 'true',
    'jwt_secret_key': os.getenv('JWT_SECRET_KEY', 'secret'),
    'frontend_url': os.getenv('FRONTEND_URL', 'http://localhost:3000'),
}

from app import main
application = main({}, **settings)
