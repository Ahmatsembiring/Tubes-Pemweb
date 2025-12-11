# Setup Frontend - Windows (Detailed Guide)

Panduan lengkap setup Job Portal Frontend di Windows.

## Step 1: Install Node.js

1. Download Node.js dari https://nodejs.org/
2. Pilih LTS version (Recommended)
3. Run installer dan follow steps:
   - Accept License
   - Choose Installation Path
   - **IMPORTANT**: Check "Add to PATH"
   - Install

4. Verify installation (buka Command Prompt baru):
   \`\`\`
   node --version
   npm --version
   \`\`\`

## Step 2: Setup Project Folder

1. Navigate ke project folder:
   \`\`\`
   cd C:\Users\YourName\Documents\job-portal\frontend
   \`\`\`

2. Pastikan struktur folder benar:
   \`\`\`
   frontend/
   ├── public/
   ├── src/
   ├── package.json
   ├── vite.config.js
   └── .env.example
   \`\`\`

## Step 3: Install Dependencies

1. Install npm packages:
   \`\`\`
   npm install
   \`\`\`

   Ini akan download semua packages dan create `node_modules/` folder.
   
   Tunggu sampai selesai (2-5 menit tergantung internet).

2. Verify (pastikan tidak ada error):
   \`\`\`
   npm list
   \`\`\`

## Step 4: Configure Environment

1. Copy file `.env.example` ke `.env`:
   \`\`\`
   copy .env.example .env
   \`\`\`

2. Edit file `.env` dengan Notepad:
   \`\`\`ini
   VITE_API_BASE_URL=http://localhost:6543
   VITE_VERCEL_BLOB_TOKEN=
   \`\`\`

## Step 5: Start Development Server

1. Run development server:
   \`\`\`
   npm run dev
   \`\`\`

2. Terminal akan output:
   \`\`\`
   VITE v5.0.0  ready in 123 ms

   ➜  Local:   http://localhost:3000/
   ➜  press h to show help
   \`\`\`

3. Open browser ke: `http://localhost:3000`

## Step 6: Verify Setup

Frontend siap jika Anda bisa:

- [ ] Akses `http://localhost:3000` tanpa error
- [ ] Lihat Home page dengan logo "JobPortal"
- [ ] Klik "Browse Jobs" redirect ke `/jobs`
- [ ] Klik "Sign Up" redirect ke `/register`

## Testing Functionality

### Test 1: Register User
1. Go to http://localhost:3000/register
2. Fill form:
   - Name: John Doe
   - Email: john@example.com
   - Role: Job Seeker
   - Password: Password123!
3. Click "Create Account"
4. Should see verification message

### Test 2: Login
1. Go to http://localhost:3000/login
2. Enter credentials dari test 1
3. Click "Login"
4. Should redirect ke `/jobs` page

### Test 3: Browse Jobs
1. Go to http://localhost:3000/jobs
2. Should see job listings
3. Try filter by location
4. Click job card untuk detail

## Build for Production

\`\`\`bash
npm run build
\`\`\`

Output ada di `dist/` folder. Upload ke hosting.

## Common Issues

### Issue: "Port 3000 already in use"

**Solution:**
\`\`\`bash
npm run dev -- --port 3001
\`\`\`

### Issue: "Cannot find module 'react'"

**Solution:**
\`\`\`bash
npm install
\`\`\`

### Issue: "API connection failed"

**Solution:**
- Check backend running: `http://localhost:6543`
- Verify `.env` file: `VITE_API_BASE_URL=http://localhost:6543`

### Issue: "Blank page / white screen"

**Solution:**
1. Open Browser DevTools (F12)
2. Check Console for errors
3. Clear cache: Ctrl+Shift+Delete
4. Refresh page: F5

## Stop Development Server

Press `Ctrl+C` di Command Prompt.

## Next Steps

1. Test API endpoints dengan Postman
2. Create sample jobs di admin panel
3. Test full user flow (register → apply → track)
4. Deploy frontend ke Vercel

## Helpful Commands

\`\`\`bash
npm run dev      # Start development server
npm run build    # Build for production
npm run preview  # Preview production build
npm install      # Install dependencies
npm update       # Update packages
npm list         # List installed packages
\`\`\`

## File Structure Explained

\`\`\`
frontend/
├── public/
│   └── index.html          # Main HTML file
├── src/
│   ├── components/         # Reusable components
│   ├── pages/             # Page components
│   ├── services/          # API service
│   ├── hooks/             # Custom React hooks
│   ├── context/           # React Context
│   ├── App.jsx            # Main component
│   ├── App.css            # App styles
│   ├── index.jsx          # React entry
│   └── index.css          # Global styles
├── node_modules/          # Dependencies (auto-generated)
├── dist/                  # Production build (auto-generated)
├── .env                   # Environment variables (create manually)
├── .env.example           # Example env file
├── package.json           # Project metadata & dependencies
├── vite.config.js         # Vite configuration
└── README.md              # Documentation
\`\`\`

## VS Code Tips

Install extensions (optional tapi recommended):
- ES7+ React/Redux/React-Native snippets
- Prettier - Code formatter
- Thunder Client (untuk test API)

## Additional Resources

- React Docs: https://react.dev
- Vite Docs: https://vitejs.dev
- Axios Docs: https://axios-http.com
- React Router: https://reactrouter.com

---

Happy coding! 🚀
