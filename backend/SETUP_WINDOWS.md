# Panduan Setup Lengkap - Job Portal System Backend di Windows

## Bagian 1: Instalasi Prerequisites

### 1.1 Install Python 3.8+

1. Download Python dari https://www.python.org/downloads/
   - Pilih versi terbaru (Python 3.11+)
   - Klik tombol Download

2. Jalankan installer `.exe`

3. **PENTING**: Di halaman pertama, centang:
   - "Add Python to PATH" ✓
   - Klik "Install Now"

4. Tunggu instalasi selesai, lalu klik "Close"

5. Verify instalasi:
   - Buka `Command Prompt` (Win+R → cmd → Enter)
   - Ketik: `python --version`
   - Expected output: `Python 3.11.x` (atau versi terbaru)

### 1.2 Install PostgreSQL

1. Download dari https://www.postgresql.org/download/windows/

2. Jalankan installer `.exe`

3. Di halaman "Setup - PostgreSQL", ikuti langkah:
   - **Installation Directory**: C:\Program Files\PostgreSQL\15 (default OK)
   - **Uncheck** "Stack Builder" (optional)
   - **Next**

4. Di halaman "Password":
   - **Set password untuk user "postgres"**: Catat baik-baik ini!
   - Contoh: `postgres123`
   - **Next**

5. **Port**: Biarkan default 5432
   - **Next** → Finish

6. Verify instalasi:
   - Buka Command Prompt
   - Ketik: `psql --version`
   - Expected output: `psql (PostgreSQL) 15.x`

---

## Bagian 2: Setup Database

1. Buka Command Prompt

2. Koneksikan ke PostgreSQL:
   \`\`\`cmd
   psql -U postgres
   \`\`\`
   - Masukkan password yang sudah dibuat
   - Prompt akan berubah menjadi `postgres=#`

3. Buat database:
   \`\`\`sql
   CREATE DATABASE job_portal_db;
   \`\`\`

4. Verify:
   \`\`\`sql
   \l
   \`\`\`
   - Anda akan melihat `job_portal_db` di list

5. Keluar dari PostgreSQL:
   \`\`\`sql
   \q
   \`\`\`

---

## Bagian 3: Setup Backend Project

### 3.1 Persiapan Folder

1. Buka Command Prompt atau PowerShell

2. Navigate ke folder project:
   \`\`\`cmd
   cd C:\Users\YourUsername\Documents\job-portal-system
   cd backend
   \`\`\`

### 3.2 Setup Virtual Environment

1. Buat virtual environment:
   \`\`\`cmd
   python -m venv venv
   \`\`\`
   - Tunggu hingga selesai (beberapa detik)

2. Activate virtual environment:
   \`\`\`cmd
   venv\Scripts\activate
   \`\`\`
   - Perhatikan: prompt akan berubah menjadi `(venv) C:\...`

3. Upgrade pip (optional tapi recommended):
   \`\`\`cmd
   python -m pip install --upgrade pip
   \`\`\`

### 3.3 Install Dependencies

1. Pastikan virtual environment masih aktif (ada `(venv)` di prompt)

2. Install packages:
   \`\`\`cmd
   pip install -r requirements.txt
   \`\`\`
   - Ini akan install: pyramid, sqlalchemy, psycopg2, jwt, bcrypt, dll
   - Tunggu hingga selesai (2-3 menit)

3. Verify instalasi:
   \`\`\`cmd
   pip list
   \`\`\`
   - Anda akan melihat semua packages yang terinstall

---

## Bagian 4: Konfigurasi Environment Variables

### 4.1 Buat file `.env`

1. Di folder `backend/`, buat file baru bernama `.env`

2. Isi dengan konfigurasi berikut:
   \`\`\`
   DB_USER=postgres
   DB_PASSWORD=postgres123
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=job_portal_db
   JWT_SECRET_KEY=job-portal-secret-key-change-this-in-production
   FRONTEND_URL=http://localhost:3000
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SENDER_EMAIL=your-email@gmail.com
   SENDER_PASSWORD=your-app-password
   \`\`\`

   Keterangan:
   - `DB_PASSWORD`: Password yang Anda buat saat install PostgreSQL
   - `JWT_SECRET_KEY`: Ganti dengan key yang lebih aman
   - `SENDER_EMAIL` & `SENDER_PASSWORD`: Setup Gmail (lihat bagian 4.2)

### 4.2 Setup Gmail untuk Email Verification (Opsional)

Jika ingin test email verification:

1. Enable 2-Factor Authentication di Google Account:
   - Buka https://myaccount.google.com/
   - Security → 2-Step Verification → Enable

2. Buat App Password:
   - Buka https://myaccount.google.com/apppasswords
   - Select: Mail & Windows Computer
   - Google akan generate password unik
   - Copy ke `.env` sebagai `SENDER_PASSWORD`

3. Atau (lebih simple untuk development):
   - Di `.env`, set: `SENDER_PASSWORD=your-regular-gmail-password`
   - Pastikan "Less Secure App Access" diaktifkan di https://myaccount.google.com/lesssecureapps

---

## Bagian 5: Jalankan Server

1. Buka Command Prompt (atau PowerShell)

2. Navigate ke folder backend:
   \`\`\`cmd
   cd backend
   \`\`\`

3. Activate virtual environment (jika belum):
   \`\`\`cmd
   venv\Scripts\activate
   \`\`\`

4. Jalankan server:
   \`\`\`cmd
   python main.py
   \`\`\`

5. Expected output:
   \`\`\`
   Server started on http://localhost:6543
   \`\`\`

6. Server sedang berjalan! Buka browser: http://localhost:6543

---

## Bagian 6: Testing API

Gunakan **Postman** atau **cURL** untuk test:

### Download Postman (Optional)
- https://www.postman.com/downloads/

### Test Register Endpoint

1. **Method**: POST
2. **URL**: `http://localhost:6543/auth/register`
3. **Body** (JSON):
   \`\`\`json
   {
     "email": "john@example.com",
     "password": "SecurePass123",
     "full_name": "John Doe",
     "role": "job_seeker"
   }
   \`\`\`
4. **Send**

### Test Login Endpoint

1. **Method**: POST
2. **URL**: `http://localhost:6543/auth/login`
3. **Body** (JSON):
   \`\`\`json
   {
     "email": "john@example.com",
     "password": "SecurePass123"
   }
   \`\`\`
4. **Send**
5. Copy token dari response

### Test Protected Endpoint (Create Job)

1. **Method**: POST
2. **URL**: `http://localhost:6543/jobs`
3. **Headers**:
   - Key: `Authorization`
   - Value: `Bearer <paste-token-disini>`
4. **Body** (JSON):
   \`\`\`json
   {
     "title": "Senior Python Developer",
     "description": "We are looking for experienced Python developers with 5+ years experience",
     "requirements": "Python, Django/FastAPI, PostgreSQL, REST API",
     "salary_min": 100000,
     "salary_max": 150000,
     "location": "Jakarta",
     "job_type": "full_time"
   }
   \`\`\`
5. **Send**

---

## Bagian 7: Troubleshooting

### Error: "postgres command not found"
- PostgreSQL belum di-add ke PATH
- Solusi: Restart Command Prompt setelah install PostgreSQL
- Atau set PATH manually (Advanced Users)

### Error: "python command not found"
- Python belum di-add ke PATH
- Solusi: Reinstall Python, pastikan "Add Python to PATH" dicek

### Error: "Database job_portal_db does not exist"
- Database belum dibuat
- Solusi: Jalankan create database command di psql

### Error: "Port 6543 already in use"
\`\`\`cmd
# Find process
netstat -ano | findstr :6543

# Kill process (ganti <PID> dengan nomor yang ditampilkan)
taskkill /PID <PID> /F
\`\`\`

### Error: "psycopg2.OperationalError: could not connect to server"
- PostgreSQL service tidak running
- Solusi: 
  1. Buka Services (services.msc)
  2. Cari "postgresql"
  3. Right-click → Start

### Virtual environment tidak activate
\`\`\`cmd
# Jika menggunakan PowerShell, mungkin perlu set execution policy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Kemudian activate lagi
venv\Scripts\activate
\`\`\`

---

## Bagian 8: Development Tips

### Menjalankan server di background (PowerShell)
\`\`\`powershell
Start-Process python main.py
\`\`\`

### Auto-restart server saat code berubah (Install first)
\`\`\`cmd
pip install watchdog
\`\`\`
Kemudian modifikasi main.py untuk pakai watchdog.

### Access database dengan PgAdmin (GUI)
1. Install PgAdmin dari https://www.pgadmin.org/download/pgadmin-4-windows/
2. Local server → Servers → Create → Server
3. Connection:
   - Host: localhost
   - Port: 5432
   - Username: postgres
   - Password: (password yang Anda buat)

---

## Ringkasan Setup Commands

Copy-paste commands ini untuk quick setup:

\`\`\`cmd
REM 1. Create virtual environment
python -m venv venv

REM 2. Activate virtual environment
venv\Scripts\activate

REM 3. Install dependencies
pip install -r requirements.txt

REM 4. Buat .env file (manual di editor)

REM 5. Run server
python main.py
\`\`\`

---

## Selanjutnya: Frontend Setup

Setelah backend berjalan, setup React frontend di folder `frontend/` dengan langkah serupa.

Untuk questions atau issues, referensi README.md yang ada di folder backend.
