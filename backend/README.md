# Job Portal System - Backend API

Pyramid-based REST API untuk Job Portal System dengan PostgreSQL, JWT Authentication, dan Email Verification.

## Prerequisites

- Python 3.8+
- PostgreSQL 12+
- pip (Python package manager)

## Setup Windows

### 1. Install Python dan PostgreSQL

**Python:**
- Download dari https://www.python.org/downloads/
- **PENTING**: Centang "Add Python to PATH" saat install
- Verify: Buka Command Prompt, ketik `python --version`

**PostgreSQL:**
- Download dari https://www.postgresql.org/download/windows/
- Catat password untuk user "postgres"
- Verify: Buka Command Prompt, ketik `psql --version`

### 2. Buat Database

\`\`\`cmd
# Buka PostgreSQL Command Line
psql -U postgres

# Create database
CREATE DATABASE job_portal_db;

# Verify
\l
\`\`\`

### 3. Setup Virtual Environment

\`\`\`cmd
# Navigate ke folder backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
\`\`\`

### 4. Konfigurasi Environment Variables

Buat file `.env` di folder `backend/`:

\`\`\`
DB_USER=postgres
DB_PASSWORD=<your-postgres-password>
DB_HOST=localhost
DB_PORT=5432
DB_NAME=job_portal_db
JWT_SECRET_KEY=your-super-secret-key-change-this
FRONTEND_URL=http://localhost:3000
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-specific-password
\`\`\`

**Setup Gmail App Password (untuk email verification):**
1. Enable 2-Factor Authentication di Google Account
2. Buka https://myaccount.google.com/apppasswords
3. Select Mail & Windows Computer
4. Copy app password ke `SENDER_PASSWORD`

### 5. Jalankan Server

\`\`\`cmd
# Pastikan virtual environment aktif
venv\Scripts\activate

# Run server
python main.py
\`\`\`

Server akan berjalan di `http://localhost:6543`

## API Endpoints

### Authentication
- `POST /auth/register` - Register user
- `POST /auth/login` - Login & get JWT token
- `POST /auth/verify-email` - Verify email dengan token

### Jobs
- `GET /jobs` - List jobs (dengan search & filter)
- `POST /jobs` - Create job (Employer only)
- `PUT /jobs/{id}` - Update job (Employer only)
- `DELETE /jobs/{id}` - Delete job (Employer only)

### Applications
- `GET /applications` - List applications
- `POST /jobs/{id}/apply` - Apply untuk job
- `GET /applications/{id}` - Get application detail
- `PUT /applications/{id}` - Update application status

### Profile
- `GET /profile` - Get current user profile
- `PUT /profile` - Update current user profile
- `GET /employers/{id}` - Get employer public profile

## Request/Response Examples

### Register (Job Seeker)
\`\`\`json
POST /auth/register
{
  "email": "john@example.com",
  "password": "SecurePass123",
  "full_name": "John Doe",
  "role": "job_seeker"
}
\`\`\`

### Register (Employer)
\`\`\`json
POST /auth/register
{
  "email": "company@example.com",
  "password": "SecurePass123",
  "full_name": "John Smith",
  "role": "employer",
  "company_name": "Tech Company Inc"
}
\`\`\`

### Login
\`\`\`json
POST /auth/login
{
  "email": "john@example.com",
  "password": "SecurePass123"
}

Response:
{
  "message": "Login successful",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "email": "john@example.com",
    "full_name": "John Doe",
    "role": "job_seeker"
  }
}
\`\`\`

### Create Job (Employer only)
\`\`\`json
POST /jobs
Authorization: Bearer <token>
{
  "title": "Senior Python Developer",
  "description": "We are looking for an experienced Python developer...",
  "requirements": "5+ years Python, FastAPI, PostgreSQL",
  "salary_min": 80000,
  "salary_max": 120000,
  "location": "Jakarta, Indonesia",
  "job_type": "full_time"
}
\`\`\`

### List Jobs dengan Filter
\`\`\`
GET /jobs?title=Python&location=Jakarta&salary_min=80000&page=1&per_page=10
\`\`\`

### Apply for Job
\`\`\`json
POST /jobs/1/apply
Authorization: Bearer <token>
{
  "cover_letter": "I am very interested in this position..."
}
\`\`\`

### Update Application Status (Employer only)
\`\`\`json
PUT /applications/1
Authorization: Bearer <token>
{
  "status": "shortlisted",
  "notes": "Qualified candidate, move to interview round"
}
\`\`\`

## Security Features

- Password hashing dengan bcrypt (12 rounds)
- JWT token authentication (24 hours expiry)
- Email verification sebelum login
- Role-based access control (Job Seeker vs Employer)
- Parameterized queries untuk prevent SQL injection
- CORS middleware untuk frontend integration

## Database Schema

**Users Table:**
- id, email, password_hash, full_name, role, is_email_verified, email_verification_token, created_at, updated_at

**Job Seekers Table:**
- id, user_id, skills, experience_years, cv_url, phone, location, bio, created_at, updated_at

**Employers Table:**
- id, user_id, company_name, company_description, company_logo_url, company_website, phone, location, created_at, updated_at

**Jobs Table:**
- id, employer_id, title, description, requirements, salary_min, salary_max, location, job_type, is_active, created_at, updated_at

**Applications Table:**
- id, job_id, job_seeker_id, status, cover_letter, notes, applied_at, updated_at

## Troubleshooting

**PostgreSQL Connection Error:**
\`\`\`
Pastikan PostgreSQL service sedang berjalan
Services Windows: postgresql-x64-15 harus "Running"
\`\`\`

**Port 6543 sudah digunakan:**
\`\`\`cmd
# Find process using port
netstat -ano | findstr :6543

# Kill process
taskkill /PID <PID> /F
\`\`\`

**Email tidak terkirim:**
- Verify SMTP credentials di .env
- Gunakan app-specific password untuk Gmail
- Check firewall settings
