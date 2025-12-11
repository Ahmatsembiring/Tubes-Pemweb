import re
from pyramid.httpexceptions import HTTPBadRequest

class Validators:
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_password(password: str) -> bool:
        """
        Validate password strength:
        - Minimum 8 characters
        - At least one uppercase
        - At least one lowercase
        - At least one digit
        """
        if len(password) < 8:
            return False
        if not re.search(r'[A-Z]', password):
            return False
        if not re.search(r'[a-z]', password):
            return False
        if not re.search(r'\d', password):
            return False
        return True
    
    @staticmethod
    def validate_registration_data(data: dict, role: str) -> dict:
        """Validate registration input"""
        errors = {}
        
        # Email validation
        email = data.get('email', '').strip()
        if not email:
            errors['email'] = 'Email is required'
        elif not Validators.validate_email(email):
            errors['email'] = 'Invalid email format'
        
        # Password validation
        password = data.get('password', '')
        if not password:
            errors['password'] = 'Password is required'
        elif not Validators.validate_password(password):
            errors['password'] = 'Password must be at least 8 characters with uppercase, lowercase, and digits'
        
        # Full name validation
        full_name = data.get('full_name', '').strip()
        if not full_name or len(full_name) < 2:
            errors['full_name'] = 'Full name must be at least 2 characters'
        
        # Role-specific validation
        if role == 'employer':
            company_name = data.get('company_name', '').strip()
            if not company_name or len(company_name) < 2:
                errors['company_name'] = 'Company name must be at least 2 characters'
        
        return errors
    
    @staticmethod
    def validate_job_data(data: dict) -> dict:
        """Validate job posting data"""
        errors = {}
        
        title = data.get('title', '').strip()
        if not title or len(title) < 5:
            errors['title'] = 'Job title must be at least 5 characters'
        
        description = data.get('description', '').strip()
        if not description or len(description) < 20:
            errors['description'] = 'Job description must be at least 20 characters'
        
        location = data.get('location', '').strip()
        if not location:
            errors['location'] = 'Location is required'
        
        # Validate salary range if provided
        salary_min = data.get('salary_min')
        salary_max = data.get('salary_max')
        if salary_min and salary_max and salary_min > salary_max:
            errors['salary'] = 'Minimum salary cannot be greater than maximum salary'
        
        return errors
