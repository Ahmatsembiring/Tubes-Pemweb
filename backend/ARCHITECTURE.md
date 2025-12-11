# Arsitektur Backend - Job Portal System

## Project Structure

\`\`\`
backend/
├── app/
│   ├── models/           # SQLAlchemy OOP Models
│   │   ├── __init__.py
│   │   ├── user.py              # Base User class + UserRole enum
│   │   ├── job_seeker.py        # JobSeeker extends User
│   │   ├── employer.py          # Employer extends User
│   │   ├── job.py               # Job + JobType enum
│   │   └── application.py       # Application + ApplicationStatus enum
│   │
│   ├── views/            # API Endpoints (Routes)
│   │   ├── __init__.py
│   │   ├── auth.py              # Register, Login, Verify Email
│   │   ├── jobs.py              # CRUD Jobs (Employer)
│   │   ├── applications.py      # Job Applications
│   │   └── profiles.py          # Profile Management
│   │
│   ├── utils/            # Helper Utilities
│   │   ├── __init__.py
│   │   ├── auth.py              # JWT token generation/verification
│   │   ├── validators.py        # Input validation
│   │   ├── email.py             # Email service
│   │   └── password.py          # Password hashing (bcrypt)
│   │
│   ├── config.py         # Database configuration
│   └── __init__.py       # Pyramid app factory
│
├── scripts/              # Database migrations (Alembic)
├── main.py              # Entry point untuk development
├── wsgi.py              # Entry point untuk production
├── setup.py             # Package configuration
├── requirements.txt     # Python dependencies
├── development.ini      # Pyramid development config
├── .env.example         # Environment variables template
└── README.md            # Documentation
\`\`\`

## Design Patterns & Best Practices

### 1. OOP Inheritance
- **Base Model**: `User` class sebagai parent
- **Subclasses**: `JobSeeker`, `Employer` extends `User`
- **Benefit**: Reusable code, easy to manage common fields

### 2. SQLAlchemy Relationships
\`\`\`python
# One-to-Many: Employer → Jobs
employer.jobs  # List all jobs by employer

# One-to-Many: Job → Applications
job.applications  # List all applications for a job

# One-to-Many: JobSeeker → Applications
job_seeker.applications  # List all applications by seeker

# Foreign Keys: Maintain data integrity
\`\`\`

### 3. Decorators for Authentication
\`\`\`python
@require_auth              # Check if user is authenticated
@require_role('employer')  # Check if user has specific role
\`\`\`

### 4. Error Handling
\`\`\`python
# Consistent JSON error responses
{
  "error": "Error message description"
}

# HTTP Status Codes:
# 200: OK
# 201: Created
# 400: Bad Request (validation error)
# 401: Unauthorized (auth required)
# 403: Forbidden (insufficient permissions)
# 404: Not Found
# 409: Conflict (email already exists)
# 500: Internal Server Error
\`\`\`

## Data Flow

### Registration Flow
1. Frontend kirim POST `/auth/register` dengan email, password, role
2. Validators validate input (email format, password strength)
3. Backend hash password dengan bcrypt
4. Create User + Profile (JobSeeker or Employer)
5. Generate email verification token
6. Send verification email
7. Return success message

### Login Flow
1. Frontend kirim POST `/auth/login` dengan email, password
2. Backend query user by email
3. Verify password menggunakan bcrypt
4. Check if email verified
5. Generate JWT token (24 hours expiry)
6. Return token + user data

### Job Posting Flow (Employer)
1. Frontend kirim POST `/jobs` dengan token
2. Middleware verify JWT token
3. Decorator check if user is employer
4. Validate job data
5. Create Job record linked to employer
6. Return job ID

### Job Application Flow (Job Seeker)
1. Frontend kirim POST `/jobs/{id}/apply` dengan token
2. Middleware verify JWT token
3. Decorator check if user is job seeker
4. Check if already applied
5. Create Application record
6. Return application ID

### Application Review Flow (Employer)
1. Frontend kirim PUT `/applications/{id}` dengan status
2. Middleware verify JWT token
3. Decorator check if user is employer
4. Verify user owns this job
5. Update application status
6. Return updated application

## Security

### Password Security
- **Algorithm**: bcrypt with 12 salt rounds
- **Hash**: Never store plain passwords
- **Verify**: Compare plain password with hashed password

### JWT Authentication
- **Token Format**: Header.Payload.Signature
- **Secret Key**: Change in production
- **Expiry**: 24 hours (can be customized)
- **Payload**: user_id, role, iat, exp

### Email Verification
- **Token**: URL-safe random string (32 characters)
- **Expiry**: Can be added (currently no expiry check)
- **Purpose**: Verify email ownership before login

### Authorization
- **Role-based**: Job Seeker vs Employer
- **Resource ownership**: Can only update own resources
- **Decorators**: @require_auth, @require_role for protection

## Database Enums

### UserRole
- `job_seeker`: Pencari kerja
- `employer`: Pemberi kerja

### JobType
- `full_time`: Full-time job
- `part_time`: Part-time job
- `contract`: Contract work
- `freelance`: Freelance project
- `internship`: Internship program

### ApplicationStatus
- `applied`: Baru apply
- `reviewed`: Sudah dilihat employer
- `shortlisted`: Lolos shortlist
- `rejected`: Ditolak
- `accepted`: Diterima

## API Response Format

### Success Response
\`\`\`json
{
  "message": "Action successful",
  "data": { /* response data */ }
}
\`\`\`

### Error Response
\`\`\`json
{
  "error": "Error description"
}
\`\`\`

### List Response (dengan pagination)
\`\`\`json
{
  "total": 50,
  "page": 1,
  "per_page": 10,
  "data": [ /* list items */ ]
}
\`\`\`

## Environment Variables

| Variable | Purpose | Example |
|----------|---------|---------|
| DB_USER | PostgreSQL user | postgres |
| DB_PASSWORD | PostgreSQL password | mypassword |
| DB_HOST | Database host | localhost |
| DB_PORT | Database port | 5432 |
| DB_NAME | Database name | job_portal_db |
| JWT_SECRET_KEY | JWT signing key | secret-key-here |
| FRONTEND_URL | Frontend URL untuk email links | http://localhost:3000 |
| SMTP_SERVER | Email SMTP server | smtp.gmail.com |
| SMTP_PORT | SMTP port | 587 |
| SENDER_EMAIL | Email sender | your@email.com |
| SENDER_PASSWORD | Email password | app-password |

## Deployment Checklist

- [ ] Change JWT_SECRET_KEY in production
- [ ] Use strong database password
- [ ] Setup Gmail App Password untuk email
- [ ] Enable HTTPS untuk production
- [ ] Setup proper CORS for frontend domain
- [ ] Configure database backups
- [ ] Setup error logging & monitoring
- [ ] Use production WSGI server (Gunicorn, uWSGI)
