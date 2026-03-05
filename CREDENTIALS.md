# College EMS - System Credentials & Access Information

## 🔐 Admin Access

### Admin Dashboard Login
- **URL**: `http://localhost:5000/pages/admin_login.html`
- **Email**: `admin@college.edu`
- **Password**: `Admin@123`

### Admin Capabilities
- View all events and registration statistics
- Generate QR codes for events
- View attendance reports (all registered students with Present/Absent status)
- Export attendance to Excel
- Search students
- View unauthorized access logs

---

## 👤 Student Access

### Student 1
- **Name**: SANJAYKUMAR M
- **Email**: `sanjaykumarmsk509@gmail.com`
- **Register Number**: `927623BCS096`
- **Password**: [Use the password you created during registration]
- **Login URL**: `http://localhost:5000/pages/login.html`
- **Registered Events**: 2 events (Data Migration, AI Workshop)

### Student 2
- **Name**: BALU
- **Email**: `pbalu1805@gmail.com`
- **Register Number**: `1026`
- **Password**: [Use the password you created during registration]
- **Login URL**: `http://localhost:5000/pages/login.html`
- **Registered Events**: 1 event (Paper Presentation)

### Student Capabilities
- Register for ONE event only (enforced)
- View registered events
- Generate QR code for attendance
- Scan QR code on event day
- View profile details

---

## 🗄️ Database Access

### MongoDB Connection
- **URI**: `mongodb://localhost:27017/`
- **Database Name**: `college_ems`
- **Collections**:
  - `students` - Student accounts and registrations
  - `events` - Event information
  - `attendance` - Attendance records (student_id + event_id + timestamp)
  - `unauthorized_log` - Unauthorized QR scan attempts

### MongoDB Shell Access
```bash
# Connect to MongoDB
mongosh

# Use database
use college_ems

# View collections
show collections

# Count documents
db.students.countDocuments()
db.events.countDocuments()
db.attendance.countDocuments()

# Find all students
db.students.find().pretty()

# Find specific student by register number
db.students.findOne({register_number: "927623BCS096"})

# Find students registered for an event
db.students.find({registered_events: ObjectId("69a5b87ed7fc256cc0914dea")})

# View all events
db.events.find().pretty()

# View attendance records
db.attendance.find().pretty()
```

---

## 🎯 Event IDs (for testing)

Based on database inspection:

1. **Paper Presentation**: `69a5b87ed7fc256cc0914dea`
2. **Coding Competition**: `69a5b87ed7fc256cc0914deb`
3. **Hackathon**: `69a5b87ed7fc256cc0914dec`
4. **Technical Quiz**: `69a5b87ed7fc256cc0914ded`
5. **Data Migration**: `69a5b87ed7fc256cc0914dee`
6. **AI Workshop**: `69a5b87ed7fc256cc0914def`

---

## 🔧 Application URLs

### Frontend Pages
- **Home**: `http://localhost:5000/`
- **Student Login**: `http://localhost:5000/pages/login.html`
- **Student Register**: `http://localhost:5000/pages/register.html`
- **Admin Login**: `http://localhost:5000/pages/admin_login.html`
- **Events Page**: `http://localhost:5000/pages/events.html` (requires login)
- **Admin Dashboard**: `http://localhost:5000/pages/admin_dashboard.html` (requires admin login)
- **Success Page**: `http://localhost:5000/pages/success.html`

### API Endpoints
- **Base URL**: `http://localhost:5000/api`
- **Auth**: `/api/auth/register`, `/api/auth/login`, `/api/auth/admin/login`
- **Student**: `/api/student/register-events`, `/api/student/my-events`, `/api/student/profile`
- **Admin**: `/api/admin/dashboard`, `/api/admin/generate-qr`, `/api/admin/attendance-report`
- **Events**: `/api/events`
- **Attendance**: `/api/attendance/mark`

---

## 🔑 JWT Tokens

### Token Structure
Tokens are JWT (JSON Web Tokens) with the following claims:

**Student Token**:
```json
{
  "student_id": "69a5cda471deaab87964dca0",
  "email": "student@email.com",
  "type": "student",
  "exp": 1234567890
}
```

**Admin Token**:
```json
{
  "email": "admin@college.edu",
  "type": "admin",
  "exp": 1234567890
}
```

### Token Usage
- Stored in `localStorage` after login
- Sent in `Authorization` header as `Bearer <token>`
- Expires after 24 hours (configurable in .env)

---

## 📧 Email Configuration (Optional)

If you want to enable email notifications:

### Gmail Setup
1. Go to Google Account > Security > 2-Step Verification (enable it)
2. Go to Google Account > Security > App passwords
3. Create new app password for "Mail" + "Windows Computer"
4. Update `.env` file:

```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=sixteen-char-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com
```

**Note**: Application works without email configuration!

---

## 🧪 Testing Scenarios

### Test 1: Student Registration Flow
1. Go to Student Register page
2. Fill in all details (name, email, register number, etc.)
3. Select department, course, year
4. Create password
5. Click Register
6. Verify redirect to login page

### Test 2: Student Login & Event Registration
1. Login with student credentials
2. View events page (should show all 6 events)
3. Select ONE event
4. Click "Register Now"
5. Verify success message
6. Check that you can't register for another event

### Test 3: Admin Dashboard
1. Login as admin
2. View dashboard statistics
3. Generate QR code for an event
4. View attendance report (should show ALL registered students)
5. Export to Excel
6. Verify data is correct

### Test 4: QR Code Attendance
1. As student, generate QR code
2. Save QR code image
3. Scan QR code (click "Scan QR Code" button)
4. Verify attendance marked
5. Check admin dashboard - attendance report should show "Present"

### Test 5: Data Type Verification
Run the check script:
```bash
cd C:\Users\sanja\project\EMS
python check_data_types.py
```

Should show:
- Event IDs in registered_events: ObjectId (not string)
- Query with ObjectId: Should find students

---

## 🐛 Known Issues & Fixes

### ✅ FIXED: Attendance Report Shows 0 Registered
**Issue**: Registration count showing 0 even when students registered
**Cause**: Data type mismatch (string vs ObjectId)
**Fix**: 
- Updated `update_registered_events()` to store ObjectId
- Updated `get_students_by_event()` to query both types
- Ran migration script to fix existing data

### ✅ FIXED: CSP Blocking API Calls
**Issue**: Content Security Policy blocking API requests
**Cause**: Hardcoded localhost URLs + Talisman in development
**Fix**:
- Changed all API URLs to relative paths (`/api`)
- Made Talisman production-only (checks `FLASK_ENV`)

---

## 🚀 Quick Start Commands

### Start Application
```bash
cd C:\Users\sanja\project\EMS
start.bat
```

### Access Admin Dashboard
1. Open browser: `http://localhost:5000/pages/admin_login.html`
2. Login: `admin@college.edu` / `Admin@123`

### Access Student Portal
1. Open browser: `http://localhost:5000/pages/login.html`
2. Login with student email and password

### Check Database
```bash
cd C:\Users\sanja\project\EMS
python check_data_types.py
```

### Run Migration (if needed)
```bash
cd C:\Users\sanja\project\EMS
python migrate_event_ids.py
```

---

## 📞 Support

For issues or questions:
- Check [SECURITY.md](SECURITY.md) for security features
- Check [RECENT_UPDATES.md](RECENT_UPDATES.md) for latest changes
- Check [CSP_FIX.md](CSP_FIX.md) for CSP/API issues
- Check [ADMIN_DATA_ACCESS_GUIDE.md](ADMIN_DATA_ACCESS_GUIDE.md) for data access

---

**Last Updated**: March 3, 2026  
**System Version**: 2.0.0  
**Status**: ✅ All Issues Fixed - Production Ready
