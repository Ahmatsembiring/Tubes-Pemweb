# Deployment Guide

Panduan deploy Frontend ke berbagai platform.

## Deploy ke Vercel (Recommended)

### Prerequisites
- GitHub account
- Project ter-push ke GitHub

### Steps

1. **Push project ke GitHub:**
   \`\`\`bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/job-portal.git
   git push -u origin main
   \`\`\`

2. **Login ke Vercel:** https://vercel.com

3. **New Project → Import GitHub Repo**

4. **Configure:**
   - Project name: `job-portal-frontend`
   - Framework: `Vite`
   - Root directory: `frontend`
   - Build command: `npm run build`
   - Output directory: `dist`

5. **Environment Variables:**
   \`\`\`
   VITE_API_BASE_URL=https://your-backend-url.com
   \`\`\`

6. **Deploy!**

## Deploy ke Netlify

1. Go to https://netlify.com
2. Login dengan GitHub
3. New site → Connect GitHub repo
4. Configure:
   - Base directory: `frontend`
   - Build command: `npm run build`
   - Publish directory: `dist`

5. Add environment variables di Netlify dashboard

## Deploy to Static Hosting (GitHub Pages)

1. Update `vite.config.js`:
   \`\`\`js
   export default {
     base: '/job-portal-frontend/',
     // ...
   }
   \`\`\`

2. Build project:
   \`\`\`bash
   npm run build
   \`\`\`

3. Deploy `dist/` folder ke GitHub Pages

## Environment Variables

Pastikan set di hosting provider:

\`\`\`
VITE_API_BASE_URL=https://your-backend-api.com
\`\`\`

## Production Checklist

- [ ] Backend API URL configured
- [ ] Token handling verified
- [ ] CORS properly setup
- [ ] SSL certificate enabled
- [ ] Environment variables set
- [ ] Build tested locally
- [ ] Error handling works
- [ ] Mobile responsive verified

---

Selamat deploy! 🚀
