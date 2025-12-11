# API Documentation - Job Portal System

## Base URL
\`\`\`
http://localhost:6543
\`\`\`

## Authentication
Semua protected endpoints memerlukan JWT token di header:
\`\`\`
Authorization: Bearer <token>
\`\`\`

---

## Endpoints

### 1. Authentication

#### Register User
\`\`\`http
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123",
  "full_name": "John Doe",
  "role": "job_seeker",
  "company_name": "Tech Corp" // Required jika role = employer
}
\`\`\`

**Response (201 Created):**
\`\`\`json
{
  "message": "Registration successful. Please check your email to verify.",
  "user_id": 1,
  "email": "user@example.com",
  "role": "job_seeker"
}
\`\`\`

---

#### Login
\`\`\`http
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123"
}
\`\`\`

**Response (200 OK):**
\`\`\`json
{
  "message": "Login successful",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "full_name": "John Doe",
    "role": "job_seeker"
  }
}
\`\`\`

---

#### Verify Email
\`\`\`http
POST /auth/verify-email
Content-Type: application/json

{
  "token": "verification_token_from_email"
}
\`\`\`

**Response (200 OK):**
\`\`\`json
{
  "message": "Email verified successfully"
}
\`\`\`

---

### 2. Jobs Management

#### List Jobs (Public)
\`\`\`http
GET /jobs?title=Python&location=Jakarta&salary_min=80000&salary_max=150000&job_type=full_time&page=1&per_page=10
\`\`\`

**Query Parameters:**
- `title` (string, optional): Filter by job title
- `location` (string, optional): Filter by location
- `salary_min` (number, optional): Minimum salary
- `salary_max` (number, optional): Maximum salary
- `job_type` (string, optional): full_time, part_time, contract, freelance, internship
- `page` (number, default: 1): Page number
- `per_page` (number, default: 10): Items per page

**Response (200 OK):**
\`\`\`json
{
  "total": 25,
  "page": 1,
  "per_page": 10,
  "jobs": [
    {
      "id": 1,
      "title": "Senior Python Developer",
      "description": "We are looking for...",
      "requirements": "5+ years Python, Django, PostgreSQL",
      "salary_min": 100000,
      "salary_max": 150000,
      "location": "Jakarta",
      "job_type": "full_time",
      "company_name": "Tech Company",
      "employer_id": 1,
      "is_active": 1,
      "created_at": "2024-01-01T10:00:00",
      "updated_at": "2024-01-01T10:00:00"
    }
  ]
}
\`\`\`

---

#### Create Job (Employer Only)
\`\`\`http
POST /jobs
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Senior Python Developer",
  "description": "We are looking for experienced Python developers with strong backend experience",
  "requirements": "5+ years Python, Django/FastAPI, PostgreSQL, REST API design",
  "salary_min": 100000,
  "salary_max": 150000,
  "location": "Jakarta",
  "job_type": "full_time"
}
\`\`\`

**Response (201 Created):**
\`\`\`json
{
  "message": "Job created successfully",
  "job": {
    "id": 1,
    "title": "Senior Python Developer",
    "description": "We are looking for...",
    "requirements": "5+ years Python...",
    "salary_min": 100000,
    "salary_max": 150000,
    "location": "Jakarta",
    "job_type": "full_time",
    "company_name": "Tech Company",
    "employer_id": 1,
    "is_active": 1,
    "created_at": "2024-01-01T10:00:00",
    "updated_at": "2024-01-01T10:00:00"
  }
}
\`\`\`

---

#### Get Job Detail
\`\`\`http
GET /jobs/{job_id}
\`\`\`

**Response (200 OK):**
\`\`\`json
{
  "id": 1,
  "title": "Senior Python Developer",
  "description": "...",
  "requirements": "...",
  "salary_min": 100000,
  "salary_max": 150000,
  "location": "Jakarta",
  "job_type": "full_time",
  "company_name": "Tech Company",
  "employer_id": 1,
  "is_active": 1,
  "created_at": "2024-01-01T10:00:00",
  "updated_at": "2024-01-01T10:00:00"
}
\`\`\`

---

#### Update Job (Employer Only)
\`\`\`http
PUT /jobs/{job_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Senior Python Developer (Updated)",
  "description": "Updated description...",
  "salary_min": 120000,
  "salary_max": 180000
}
\`\`\`

**Response (200 OK):**
\`\`\`json
{
  "message": "Job updated successfully",
  "job": { /* updated job data */ }
}
\`\`\`

---

#### Delete Job (Employer Only)
\`\`\`http
DELETE /jobs/{job_id}
Authorization: Bearer <token>
\`\`\`

**Response (200 OK):**
\`\`\`json
{
  "message": "Job deleted successfully"
}
\`\`\`

---

### 3. Applications

#### Get Applications
\`\`\`http
GET /applications?status=applied&page=1&per_page=10
Authorization: Bearer <token>
\`\`\`

**Note:**
- Employer: Lihat semua aplikasi untuk jobs mereka
- Job Seeker: Lihat aplikasi mereka sendiri

**Query Parameters:**
- `status` (string, optional): applied, reviewed, shortlisted, rejected, accepted
- `page` (number, default: 1)
- `per_page` (number, default: 10)

**Response (200 OK):**
\`\`\`json
{
  "total": 5,
  "page": 1,
  "per_page": 10,
  "applications": [
    {
      "id": 1,
      "job_id": 1,
      "job_title": "Senior Python Developer",
      "job_seeker_id": 2,
      "seeker_name": "Jane Smith",
      "seeker_email": "jane@example.com",
      "status": "applied",
      "cover_letter": "I am interested in this position...",
      "notes": null,
      "applied_at": "2024-01-01T10:00:00",
      "updated_at": "2024-01-01T10:00:00"
    }
  ]
}
\`\`\`

---

#### Apply for Job (Job Seeker Only)
\`\`\`http
POST /jobs/{job_id}/apply
Authorization: Bearer <token>
Content-Type: application/json

{
  "cover_letter": "I am very interested in this position because..."
}
\`\`\`

**Response (201 Created):**
\`\`\`json
{
  "message": "Application submitted successfully",
  "application": { /* application data */ }
}
\`\`\`

---

#### Update Application Status (Employer Only)
\`\`\`http
PUT /applications/{application_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "status": "shortlisted",
  "notes": "Good candidate, proceed to phone screening"
}
\`\`\`

**Status Options:** applied, reviewed, shortlisted, rejected, accepted

**Response (200 OK):**
\`\`\`json
{
  "message": "Application updated successfully",
  "application": { /* updated application data */ }
}
\`\`\`

---

### 4. Profiles

#### Get Current User Profile
\`\`\`http
GET /profile
Authorization: Bearer <token>
\`\`\`

**Response (200 OK):**
\`\`\`json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "full_name": "John Doe",
    "role": "job_seeker",
    "is_email_verified": true,
    "created_at": "2024-01-01T10:00:00"
  },
  "profile": {
    "id": 1,
    "user_id": 1,
    "skills": "Python, JavaScript, React, PostgreSQL",
    "experience_years": 5,
    "cv_url": "https://storage.example.com/cv.pdf",
    "phone": "08123456789",
    "location": "Jakarta",
    "bio": "Passionate developer with 5+ years experience",
    "created_at": "2024-01-01T10:00:00"
  }
}
\`\`\`

---

#### Update Profile
\`\`\`http
PUT /profile
Authorization: Bearer <token>
Content-Type: application/json

{
  "full_name": "John Doe Updated",
  "skills": "Python, JavaScript, React, PostgreSQL, Django",
  "experience_years": 6,
  "phone": "08123456789",
  "location": "Jakarta, Indonesia",
  "bio": "Updated bio"
}
\`\`\`

**For Employer:**
\`\`\`json
{
  "company_name": "Tech Company Updated",
  "company_description": "We build innovative software...",
  "company_logo_url": "https://storage.example.com/logo.png",
  "company_website": "https://techcompany.com",
  "phone": "021123456",
  "location": "Jakarta Selatan"
}
\`\`\`

**Response (200 OK):**
\`\`\`json
{
  "message": "Profile updated successfully",
  "user": { /* user data */ },
  "profile": { /* updated profile */ }
}
\`\`\`

---

#### Get Employer Profile
\`\`\`http
GET /employers/{employer_id}
\`\`\`

**Response (200 OK):**
\`\`\`json
{
  "employer": {
    "id": 1,
    "user_id": 1,
    "company_name": "Tech Company",
    "company_description": "...",
    "company_logo_url": "...",
    "company_website": "https://techcompany.com",
    "phone": "021123456",
    "location": "Jakarta",
    "created_at": "2024-01-01T10:00:00"
  },
  "user": {
    "id": 1,
    "email": "employer@example.com",
    "full_name": "John Smith",
    "role": "employer",
    "created_at": "2024-01-01T10:00:00"
  }
}
\`\`\`

---

## Error Responses

### Validation Error (400)
\`\`\`json
{
  "error": "{\"email\": \"Invalid email format\", \"password\": \"Password must be at least 8 characters...\"}"
}
\`\`\`

### Unauthorized (401)
\`\`\`json
{
  "error": "Invalid email or password"
}
\`\`\`

### Forbidden (403)
\`\`\`json
{
  "error": "Not authorized to update this job"
}
\`\`\`

### Not Found (404)
\`\`\`json
{
  "error": "Job not found"
}
\`\`\`

### Conflict (409)
\`\`\`json
{
  "error": "Email already registered"
}
\`\`\`

---

## Testing with cURL

### Register
\`\`\`bash
curl -X POST http://localhost:6543/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "SecurePass123",
    "full_name": "John Doe",
    "role": "job_seeker"
  }'
\`\`\`

### Login
\`\`\`bash
curl -X POST http://localhost:6543/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "SecurePass123"
  }'
\`\`\`

### List Jobs
\`\`\`bash
curl -X GET "http://localhost:6543/jobs?location=Jakarta&page=1" \
  -H "Content-Type: application/json"
\`\`\`

### Create Job (dengan token)
\`\`\`bash
curl -X POST http://localhost:6543/jobs \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "title": "Python Developer",
    "description": "...",
    "salary_min": 100000,
    "salary_max": 150000,
    "location": "Jakarta",
    "job_type": "full_time"
  }'
