# Job Portal System - Full Stack

Platform lowongan kerja dengan job posting, aplikasi, dan tracking pelamar.

## Project Structure

Ini adalah **full-stack application** dengan dua server terpisah:

\`\`\`
job-portal/
├── backend/                 # Python Pyramid API Server
│   ├── app/
│   ├── main.py
│   ├── requirements.txt
│   └── README.md
│
├── frontend/                # React.js Client (Vite)
│   ├── src/
│   ├── package.json
│   ├── vite.config.js
│   └── README.md
│
└── README.md               # This file
\`\`\`

## Quick Start

### Prerequisites
- Python 3.8+ & PostgreSQL 12+ (untuk backend)
- Node.js 16+ (untuk frontend)

### Option 1: Run Backend Only (Testing API)

\`\`\`bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
\`\`\`

Backend berjalan di: `http://localhost:6543`

### Option 2: Run Frontend Only (Testing UI)

\`\`\`bash
cd frontend
npm install
npm run dev
\`\`\`

Frontend berjalan di: `http://localhost:3000`

### Option 3: Run Both (Full Application)

**Terminal 1 - Backend:**
\`\`\`bash
cd backend
venv\Scripts\activate
python main.py
\`\`\`

**Terminal 2 - Frontend:**
\`\`\`bash
cd frontend
npm run dev
\`\`\`

Open browser: `http://localhost:3000`

## Architecture

- **Backend:** Python Pyramid + SQLAlchemy + PostgreSQL
  - RESTful API dengan JWT authentication
  - Database models dengan OOP inheritance
  - Email verification, password hashing
  - Role-based access control

- **Frontend:** React 18 + Vite + Vanilla CSS
  - SPA dengan React Router
  - State management dengan Context API
  - Responsive mobile-first design
  - Token-based authentication

## Tech Stack

| Component | Technology |
|-----------|------------|
| Backend API | Python Pyramid 2.0 |
| Database | PostgreSQL 12+ |
| ORM | SQLAlchemy |
| Frontend | React 18 |
| Build Tool | Vite 5 |
| Styling | Vanilla CSS |
| HTTP Client | Axios |
| Authentication | JWT |

## Features

- User registration & email verification
- Job CRUD operations
- Job applications tracking
- Application management (accept/reject/shortlist)
- User profile management
- CV upload to Vercel Blob
- Search & filter jobs
- Role-based access (Job Seeker / Employer)

## Documentation

### Backend
- [Backend Setup Guide](backend/SETUP_WINDOWS.md)
- [Backend README](backend/README.md)
- [API Documentation](backend/API_DOCUMENTATION.md)
- [Architecture Overview](backend/ARCHITECTURE.md)

### Frontend
- [Frontend Setup Guide](frontend/SETUP_WINDOWS.md)
- [Frontend README](frontend/README.md)
- [Deployment Guide](frontend/DEPLOYMENT.md)

## Setup Instructions

### Windows Setup Step by Step

1. **Install Requirements**
   - Python 3.8+ dari python.org
   - PostgreSQL dari postgresql.org
   - Node.js dari nodejs.org

2. **Backend Setup**
   \`\`\`bash
   cd backend
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   copy .env.example .env
   # Edit .env dengan database config
   python main.py
   \`\`\`

3. **Frontend Setup**
   \`\`\`bash
   cd frontend
   npm install
   copy .env.example .env
   npm run dev
   \`\`\`

4. **Test Full Application**
   - Open `http://localhost:3000`
   - Register akun baru
   - Browse jobs atau post job
   - Test full workflow

## API Endpoints

Base URL: `http://localhost:6543`

### Authentication
- `POST /auth/register` - Register user
- `POST /auth/login` - Login
- `GET /auth/verify-email/:token` - Verify email

### Jobs
- `GET /jobs` - List jobs with filter
- `POST /jobs` - Create job (employer)
- `PUT /jobs/:id` - Update job
- `DELETE /jobs/:id` - Delete job
- `GET /jobs/:id` - Job detail

### Applications
- `POST /jobs/:id/apply` - Apply job
- `GET /applications` - List applications
- `PUT /applications/:id` - Update status

### Profile
- `GET /profile` - Get profile
- `PUT /profile` - Update profile

## Troubleshooting

### Backend Issues
- **Port 6543 in use:** Change port di `backend/main.py`
- **Database connection failed:** Verify PostgreSQL running & credentials
- **Import errors:** Ensure venv activated & requirements installed

### Frontend Issues
- **Port 3000 in use:** Run `npm run dev -- --port 3001`
- **API not connecting:** Check backend running & VITE_API_BASE_URL correct
- **Module not found:** Run `npm install`

## Database Setup

Buat database PostgreSQL:

\`\`\`sql
createdb job_portal_db
\`\`\`

Atau via pgAdmin.

## Deployment

### Backend
- Deploy ke AWS, Heroku, atau VPS
- Set environment variables
- Configure database connection
- Update CORS origins

### Frontend
- Build: `npm run build`
- Deploy ke Vercel, Netlify, atau static hosting
- Update API_BASE_URL untuk production

## Development Workflow

1. Buat branch feature: `git checkout -b feature/nama-feature`
2. Develop di backend atau frontend
3. Test secara lokal
4. Create pull request
5. Merge ke main

## Performance Optimization

- Frontend: Code splitting dengan React.lazy
- Backend: Database query optimization dengan SQLAlchemy
- Caching: Redis untuk session management
- Frontend assets: Minified & optimized

## Security Best Practices

- Password hashing dengan bcrypt
- JWT token management
- CORS properly configured
- SQL injection prevention dengan parameterized queries
- Input validation & sanitization
- Row-level security (Supabase jika menggunakan)

## Support & Issues

Jika ada masalah:
1. Check dokumentasi di folder masing-masing
2. Review error messages di browser console & server logs
3. Verify environment variables
4. Check database connection
5. Create issue dengan detail error

## License

MIT

## Author

Developed for Job Portal System Learning Project

---

**Happy coding! Start dengan `npm run dev` di frontend folder.** 🚀
