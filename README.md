# College Event Management System with QR Code Attendance

A production-quality web application for managing college events and tracking attendance using secure QR code technology.

## 🎯 Features

### Authentication & Registration
- **Student Registration** with complete validation
- **Student Login** with JWT token-based authentication
- **Admin Login** with secure credentials
- **Bcrypt password hashing** for security

### Event Management
- Pre-configured events (Paper Presentation, Coding Contest, Gaming Tournament, etc.)
- Students can select and register for multiple events
- Event capacity tracking
- Real-time registration statistics

### QR Code Attendance System
- **Secure QR code generation** with token-based verification
- **QR code scanning** for attendance marking
- **Duplicate prevention** - attendance can only be marked once per event
- **Unauthorized access logging** - tracks invalid scan attempts
- **Time-stamped attendance records**

### Admin Dashboard
- **Comprehensive statistics**:
  - Total registered students
  - Event-wise registrations
  - Department-wise statistics
  - Attendance percentages
- **QR code generation** for events
- **Attendance reports** with detailed breakdowns
- **Excel export** functionality for attendance data
- **Student search** by register number
- **Unauthorized scan logs** monitoring

### Notification System
- **Email confirmations** for:
  - Event registration
  - Attendance marking
- HTML-formatted emails with modern templates

### Security Features
- JWT token-based authentication
- Bcrypt password hashing
- Input validation and sanitization
- Rate limiting to prevent abuse
- XSS protection
- Duplicate registration prevention
- Secure QR token generation
- Unauthorized access logging

## 🛠️ Tech Stack

### Backend
- **Python Flask** - Web framework
- **Supabase (PostgreSQL)** - Database backend (replaces MongoDB)
- **PyJWT** - JWT token handling
- **Bcrypt** - Password hashing
- **QRCode** - QR code generation
- **Flask-CORS** - Cross-origin resource sharing
- **Flask-Limiter** - Rate limiting
- **OpenPyXL** - Excel file generation

### Frontend
- **HTML5** - Structure
- **CSS3** - Modern, responsive styling
- **JavaScript (ES6+)** - Interactive functionality
- **Fetch API** - Asynchronous communication
- **html5-qrcode** - Live QR code scanning from camera

## 📁 Project Structure

```
EMS/
├── backend/
│   ├── app.py                  # Main Flask application
│   ├── config.py               # Configuration settings
│   ├── requirements.txt        # Python dependencies
│   ├── models/                 # Database models
│   │   ├── __init__.py
│   │   ├── student.py
│   │   ├── event.py
│   │   ├── attendance.py
│   │   └── unauthorized_log.py
│   ├── routes/                 # API routes
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── student.py
│   │   ├── admin.py
│   │   └── attendance.py
│   └── utils/                  # Utility functions
│       ├── __init__.py
│       ├── qr_generator.py
│       ├── email_service.py
│       └── validators.py
├── frontend/
│   ├── index.html              # Landing page
│   ├── css/
│   │   └── style.css           # Comprehensive styles
│   ├── js/
│   │   ├── login.js
│   │   ├── register.js
│   │   ├── events.js
│   │   ├── scan.js
│   │   └── admin.js
│   └── pages/
│       ├── login.html
│       ├── register.html
│       ├── events.html
│       ├── success.html
│       ├── admin_login.html
│       ├── admin_dashboard.html
│       └── scan.html
├── .env.example                # Environment variables template
└── README.md                   # This file
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.13 or higher
- Supabase account (free tier available at https://supabase.com)
- pip (Python package manager)

### Step 1: Clone the Repository
```bash
cd c:\Users\balasubramaniyan\team project
```

### Step 2: Create Supabase Project
1. Go to https://supabase.com and create a free account
2. Create a new project
3. In SQL Editor, run `backend/supabase_schema.sql` to create tables:
   - students
   - events
   - attendance
   - unauthorized_logs

### Step 3: Install Python Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
1. Copy `.env.example` to `backend/.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `backend/.env` and configure:
   ```env
   # Flask Configuration
   SECRET_KEY=your-secret-key-here
   JWT_SECRET_KEY=your-jwt-secret-key-here
   
   # Supabase Configuration (Required)
   USE_SUPABASE=true
   SUPABASE_URL=https://your-project-ref.supabase.co
   SUPABASE_KEY=your_anon_key_from_supabase
   
   # Admin Credentials
   ADMIN_EMAIL=admin@college.edu
   ADMIN_PASSWORD=Admin@123
   
   # Email Configuration (Optional)
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-app-password
   MAIL_DEFAULT_SENDER=noreply@collegeems.com
   ```

### Step 5: Optional - Migrate Data from MongoDB
If you have existing MongoDB data:
```bash
cd backend
python migrate_to_supabase.py
```

### Step 6: Run the Application
```bash
cd backend
python app.py
```

The application will start on `http://localhost:5000`

## 📖 Usage Guide

### For Students

1. **Registration**
   - Navigate to the registration page
   - Fill in all required details:
     - Name
     - Register Number (unique)
     - Department
     - Year (1-4)
     - Email (unique)
     - Phone Number (10 digits)
     - Password (min 6 chars, letters + numbers)
   - Submit to create account

2. **Login**
   - Use registered email and password
   - Upon successful login, you'll be redirected to event selection

3. **Event Registration**
   - Browse available events
   - Select events you want to participate in
   - Submit registration
   - Receive confirmation email

4. **Mark Attendance**
   - On event day, scan the QR code displayed at venue
   - Paste the QR data in the attendance page
   - Click "Mark Attendance"
   - Receive confirmation email

### For Administrators

1. **Admin Login**
   - Default credentials:
     - Email: `admin@college.edu`
     - Password: `Admin@123`
   - **⚠️ Change these in production!**

2. **Dashboard Overview**
   - View total students, events, and unauthorized scans
   - Monitor event-wise registrations
   - Check department-wise statistics

3. **Generate QR Code**
   - Select an event from dropdown
   - Click "Generate QR Code"
   - Download and display QR code at event venue

4. **View Reports**
   - Select an event
   - Click "View Report" to see attendance details
   - Export to Excel for offline analysis

5. **Search Students**
   - Enter register number
   - View student details and registered events

6. **Monitor Security**
   - Check unauthorized scan logs
   - Track suspicious activities

## 🔒 Security Best Practices

### For Production Deployment:

1. **Change Default Credentials**
   ```env
   ADMIN_EMAIL=your-admin-email@domain.com
   ADMIN_PASSWORD=StrongPassword123!@#
   ```

2. **Use Strong Secret Keys**
   ```python
   import secrets
   print(secrets.token_urlsafe(32))  # Generate secure keys
   ```

3. **Configure HTTPS**
   - Use SSL/TLS certificates
   - Enable HTTPS redirect

4. **Database Security**
   - Enable MongoDB authentication
   - Use strong database passwords
   - Restrict database access

5. **Email Configuration**
   - Use app-specific passwords for Gmail
   - Consider using dedicated email service (SendGrid, AWS SES)

6. **Rate Limiting**
   - Adjust rate limits in `config.py` based on your needs
   - Monitor for abuse

7. **CORS Configuration**
   - Update CORS settings in `app.py` to allow only your domain

## 🌐 API Endpoints

### Authentication
- `POST /api/auth/register` - Student registration
- `POST /api/auth/login` - Student login
- `POST /api/auth/admin/login` - Admin login
- `GET /api/auth/verify` - Verify JWT token

### Student
- `GET /api/student/events` - Get all events
- `POST /api/student/register-events` - Register for events
- `GET /api/student/my-events` - Get registered events
- `GET /api/student/profile` - Get student profile
- `GET /api/student/search/<register_number>` - Search student (admin)

### Admin
- `GET /api/admin/dashboard` - Get dashboard statistics
- `POST /api/admin/generate-qr/<event_id>` - Generate QR code
- `GET /api/admin/attendance-report/<event_id>` - Get attendance report
- `GET /api/admin/export-attendance/<event_id>` - Export to Excel
- `GET /api/admin/unauthorized-logs` - Get unauthorized logs
- `GET /api/admin/attendance-statistics` - Get detailed stats

### Attendance
- `POST /api/attendance/scan` - Mark attendance via QR scan
- `POST /api/attendance/verify-qr` - Verify QR code validity
- `GET /api/attendance/my-attendance` - Get student attendance

## 📊 Database Collections

### students
```javascript
{
  _id: ObjectId,
  name: String,
  register_number: String (unique),
  department: String,
  year: Number,
  email: String (unique),
  phone_number: String,
  password: String (hashed),
  registered_events: [ObjectId],
  created_at: DateTime,
  updated_at: DateTime
}
```

### events
```javascript
{
  _id: ObjectId,
  event_name: String,
  description: String,
  date: String,
  venue: String,
  max_participants: Number,
  total_registered: Number,
  created_at: DateTime,
  updated_at: DateTime
}
```

### attendance
```javascript
{
  _id: ObjectId,
  student_id: ObjectId,
  event_id: ObjectId,
  qr_token: String,
  marked_at: DateTime,
  status: String
}
```

### unauthorized_logs
```javascript
{
  _id: ObjectId,
  qr_token: String,
  ip_address: String,
  user_agent: String,
  scan_data: Object,
  scanned_at: DateTime,
  status: String
}
```

## 🎨 Features Highlights

### Responsive Design
- Mobile-friendly interface
- Tablet-optimized layouts
- Desktop-first approach

### Modern UI/UX
- Clean and intuitive interface
- Smooth animations
- Color-coded status indicators
- Interactive hover effects

### Real-time Updates
- Live dashboard statistics
- Instant feedback messages
- Dynamic content loading

### Validation
- Client-side form validation
- Server-side data validation
- Comprehensive error messages

## 🚀 Deployment

For production deployment to Vercel (frontend) and your chosen backend platform, see [VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md).

### Quick Summary:
- **Frontend**: Deploy to Vercel (static site)
- **Backend**: Deploy to Heroku, Railway, AWS, Google Cloud, or self-hosted
- **Database**: Supabase (PostgreSQL) handles data persistence

## 🐛 Troubleshooting

### Supabase Connection Issues
```bash
# Test Supabase connectivity
python -c "from supabase_client import get_supabase_client; c = get_supabase_client(); print(c.rest_url)"
```

### Port Already in Use
```bash
# Kill process on port 5000 (Windows)
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Kill process on port 5000 (Linux/Mac)
lsof -ti:5000 | xargs kill -9
```

### Email Not Sending
- Verify SMTP credentials in `.env`
- Enable "Less secure app access" for Gmail
- Use app-specific passwords
- Check firewall settings

### QR Code Scanning Issues
- Ensure camera permissions are granted in browser
- Check browser console for errors
- Test with different QR codes
- Verify backend is returning valid QR tokens

## 📝 Default Events

The system comes pre-configured with:
1. Paper Presentation
2. Coding Contest
3. Gaming Tournament
4. Technical Quiz
5. Project Expo
6. Debugging Challenge

## 🔄 Future Enhancements

- [ ] Real-time WebSocket notifications
- [ ] Mobile app (React Native)
- [ ] Facial recognition attendance
- [ ] SMS notifications
- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] Certificate generation
- [ ] Payment integration for paid events

## 👥 Contributors

Built with ❤️ for educational purposes

## 📄 License

This project is for educational purposes. Feel free to use and modify.

## 📞 Support

For issues or questions, please create an issue in the repository.

---

**⚡ Quick Start Command:**
```bash
cd backend
pip install -r requirements.txt
python app.py
```

**🌐 Access the application at:** `http://localhost:5000`

**🔐 Default Admin Credentials:**
- Email: `admin@college.edu`
- Password: `Admin@123`

**⚠️ Remember to change admin credentials in production!**
