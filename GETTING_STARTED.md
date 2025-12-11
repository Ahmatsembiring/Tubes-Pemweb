# Getting Started - Job Portal System

Panduan cepat untuk mulai develop.

## 1. Setup Backend (First Time)

\`\`\`bash
cd backend

# Create virtual environment
python -m venv venv

# Activate venv
venv\Scripts\activate

# Install packages
pip install -r requirements.txt

# Setup database
# Buat database PostgreSQL terlebih dahulu
createdb job_portal_db

# Copy environment file
copy .env.example .env

# Edit .env dengan database credentials Anda
notepad .env

# Run server
python main.py
\`\`\`

✅ Backend running di `http://localhost:6543`

## 2. Setup Frontend (First Time)

\`\`\`bash
cd frontend

# Install packages
npm install

# Copy environment file
copy .env.example .env

# Start development server
npm run dev
\`\`\`

✅ Frontend running di `http://localhost:3000`

## 3. Next Time (Quick Start)

**Backend:**
\`\`\`bash
cd backend
venv\Scripts\activate
python main.py
\`\`\`

**Frontend:**
\`\`\`bash
cd frontend
npm run dev
\`\`\`

## 4. Test Application

1. Open `http://localhost:3000`
2. Click "Sign Up"
3. Register sebagai Job Seeker
4. Check email untuk verification link
5. Login dengan akun Anda
6. Browse jobs atau create profile

## 5. Useful Commands

### Backend
\`\`\`bash
pip install <package>    # Install package
pip freeze               # List packages
python main.py          # Run server
\`\`\`

### Frontend
\`\`\`bash
npm install             # Install packages
npm run dev            # Development server
npm run build          # Production build
npm run preview        # Preview build
npm list              # List packages
\`\`\`

## 6. Common Tasks

### Add new API endpoint
1. Create view di `backend/app/views/`
2. Add function dengan decorator `@view_config`
3. Test dengan Postman

### Add new page
1. Create `.jsx` file di `frontend/src/pages/`
2. Import ke `App.jsx`
3. Add route di `<Routes>`

### Update database
1. Modify model di `backend/app/models/`
2. Create migration: `alembic revision --autogenerate`
3. Apply: `alembic upgrade head`

## 7. Debugging

### Backend Debug
- Check logs di terminal
- Use `print()` untuk debug
- Test endpoints dengan Postman

### Frontend Debug
- Open DevTools: F12
- Check Console tab untuk errors
- Use `console.log()` untuk debug

## 8. Project Structure

\`\`\`
job-portal/
├── backend/              # Python Pyramid API
│   ├── app/
│   │   ├── models/      # Database models
│   │   ├── views/       # API endpoints
│   │   ├── utils/       # Helper functions
│   │   └── config.py    # Configuration
│   └── main.py          # Entry point
│
└── frontend/             # React.js Client
    ├── src/
    │   ├── pages/       # Page components
    │   ├── components/  # Reusable components
    │   ├── services/    # API calls
    │   ├── hooks/       # Custom hooks
    │   └── context/     # Context API
    └── vite.config.js   # Vite config
\`\`\`

## 9. Next Steps

- Read backend README: `backend/README.md`
- Read frontend README: `frontend/README.md`
- Check API docs: `backend/API_DOCUMENTATION.md`
- Start developing!

---

**Questions? Check the detailed setup guides in each folder.** 📚
