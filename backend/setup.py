from setuptools import setup, find_packages

setup(
    name='job_portal_system',
    version='1.0',
    description='Job Portal System Backend API',
    packages=find_packages(),
    install_requires=[
        'pyramid>=2.0',
        'pyramid-cors',
        'SQLAlchemy>=2.0',
        'psycopg2-binary',
        'PyJWT',
        'bcrypt',
        'python-dotenv',
        'waitress',
    ],
    entry_points={
        'paste.app_factory': [
            'main = app:main',
        ],
    },
)
