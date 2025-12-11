# Job Portal - Frontend

React.js frontend untuk aplikasi Job Portal System. Frontend ini menggunakan vanilla CSS dan JavaScript pure untuk state management.

## Tech Stack

- **React 18** - UI library
- **React Router v6** - Routing
- **Axios** - HTTP client
- **Vite** - Build tool
- **Vanilla CSS** - Styling (no frameworks)

## Project Structure

\`\`\`
src/
├── components/              # Reusable components
│   ├── Navbar.jsx          # Navigation bar
│   ├── ProtectedRoute.jsx  # Route protection
│   ├── LoadingSpinner.jsx  # Loading indicator
│   ├── ErrorAlert.jsx      # Error messages
│   └── FormInput.jsx       # Form input wrapper
├── pages/                   # Page components
│   ├── Home.jsx            # Landing page
│   ├── Register.jsx        # Register page
│   ├── Login.jsx           # Login page
│   ├── JobBrowser.jsx      # Job listing
│   ├── JobDetail.jsx       # Job details
│   ├── PostJob.jsx         # Post job (employer)
│   ├── ManageJobs.jsx      # Job management
│   ├── MyApplications.jsx  # Applications (seeker)
│   ├── ManageApplications.jsx # Applications (employer)
│   ├── Profile.jsx         # User profile
│   └── NotFound.jsx        # 404 page
├── services/               # API integration
│   └── api.js             # Axios instance & config
├── hooks/                  # Custom hooks
│   ├── useAuth.js         # Auth context hook
│   └── useFetch.js        # Data fetching hook
├── context/               # React Context
│   └── AuthContext.js     # Auth state
├── App.jsx                # Main app component
└── index.jsx              # Entry point
\`\`\`

## Setup Instructions (Windows)

### Prerequisites

1. **Node.js 16+**
   - Download: https://nodejs.org/
   - Verify: `node --version` & `npm --version`

2. **Backend API Running**
   - Ensure Pyramid backend is running on `http://localhost:6543`

### Installation Steps

1. **Navigate to frontend folder**
   \`\`\`bash
   cd frontend
   \`\`\`

2. **Install dependencies**
   \`\`\`bash
   npm install
   \`\`\`

3. **Create environment file**
   \`\`\`bash
   copy .env.example .env
   \`\`\`

4. **Configure `.env`**
   \`\`\`
   VITE_API_BASE_URL=http://localhost:6543
   VITE_VERCEL_BLOB_TOKEN=your_token_if_needed
   \`\`\`

5. **Start development server**
   \`\`\`bash
   npm run dev
   \`\`\`

   Server akan berjalan di: `http://localhost:3000`

6. **Build for production**
   \`\`\`bash
   npm run build
   \`\`\`

   Output akan ada di `dist/` folder

## Features

### Authentication
- User registration dengan email verification
- Login dengan JWT token
- Protected routes berdasarkan role
- Auto logout pada token expired

### Job Management
- Browse dan search jobs
- Filter by location, type, salary
- View job details
- Apply for jobs (seeker)
- Post jobs (employer)
- Manage posted jobs

### Application Management
- View applications (seeker)
- Review applicants (employer)
- Accept/Reject/Shortlist applicants

### User Profile
- Update profile information
- Upload CV/Resume
- Manage skills & experience

## API Integration

Semua API calls menggunakan Axios dari `src/services/api.js`. Token JWT secara otomatis ditambahkan ke setiap request.

**Base URL:** `http://localhost:6543`

### Key Endpoints
- `POST /auth/register` - Register user
- `POST /auth/login` - Login
- `GET /jobs` - List jobs
- `POST /jobs` - Post job (employer)
- `POST /jobs/:id/apply` - Apply job
- `GET /applications` - View applications
- `PUT /profile` - Update profile

## State Management

- **AuthContext** - Global auth state
- **useState** - Local component state
- **useFetch** - Data fetching hook dengan caching

## Styling

- **Vanilla CSS** - Semua styling menggunakan file `.css` terpisah
- **CSS Variables** - Untuk consistent colors & spacing
- **Mobile-First** - Responsive design dengan media queries
- **Flexbox & Grid** - Modern layout techniques

## Components Overview

### Navbar
Navigation bar dengan menu responsif, auth state, dan role-based navigation.

### ProtectedRoute
Wrapper untuk route yang memerlukan authentication atau role tertentu.

### FormInput
Reusable input component dengan validation dan error handling.

### LoadingSpinner
Loading indicator dengan berbagai ukuran.

### ErrorAlert
Alert component untuk menampilkan error messages.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Port 3000 already in use | `npm run dev -- --port 3001` |
| API connection failed | Pastikan backend running di localhost:6543 |
| Token expired | Clear localStorage dan login ulang |
| CORS error | Verifikasi CORS di backend sudah enabled |

## Performance Tips

- Components menggunakan React.lazy untuk code splitting
- Axios request interceptor handle JWT token
- useFetch hook implement caching
- CSS menggunakan transitions untuk smooth animations

## Deployment

Untuk deploy ke Vercel atau hosting lain:

\`\`\`bash
npm run build
\`\`\`

Upload folder `dist/` ke hosting platform.

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## License

MIT

## Support

Jika ada issues atau pertanyaan, buat issue di repository atau hubungi tim development.
