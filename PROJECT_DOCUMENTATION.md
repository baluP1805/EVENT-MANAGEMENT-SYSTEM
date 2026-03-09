# College Event Management System - Complete Project Documentation

**Version:** 1.0  
**Last Updated:** March 3, 2026  
**Status:** Production Ready ✅

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Technology Stack](#technology-stack)
4. [System Architecture](#system-architecture)
5. [Installation & Setup](#installation--setup)
6. [Configuration](#configuration)
7. [Running the Application](#running-the-application)
8. [User Guide](#user-guide)
9. [Admin Guide](#admin-guide)
10. [API Documentation](#api-documentation)
11. [Security Features](#security-features)
12. [Database Schema](#database-schema)
13. [Deployment Guide](#deployment-guide)
14. [Troubleshooting](#troubleshooting)
15. [Credentials & Access](#credentials--access)
16. [Development](#development)
17. [Maintenance](#maintenance)

---

## Project Overview

### Description

The **College Event Management System (EMS)** is a comprehensive web application designed to manage college events, student registrations, and attendance tracking using QR code technology. The system provides a secure, user-friendly platform for students to register for events and administrators to manage events and track attendance.

### Key Objectives

- **Streamline Event Management:** Simplify the process of creating and managing college events
- **Automate Attendance:** Use QR code technology for quick and accurate attendance tracking
- **Secure Registration:** Provide secure student registration and authentication
- **Real-time Reporting:** Generate instant attendance reports and statistics
- **Data Export:** Export attendance data to Excel for further analysis

### Target Users

1. **Students:** Register for events, view event details, scan QR codes for attendance
2. **Administrators:** Create events, generate QR codes, view attendance reports, export data
3. **Event Coordinators:** Monitor registrations and attendance in real-time

---

## Features

### Student Features

✅ **User Registration & Authentication**
- Secure account creation with email verification
- JWT-based authentication
- Profile management
- Password encryption with bcrypt

✅ **Event Management**
- Browse available events
- View event details (date, venue, description, capacity)
- Register for multiple events
- View registration history

✅ **QR Code Attendance**
- Scan event QR codes for attendance marking
- Real-time attendance confirmation
- View personal attendance history
- Duplicate scan prevention

✅ **Profile Dashboard**
- View personal information
- See registered events
- Track attendance records

### Admin Features

✅ **Event Management**
- Create new events
- Edit event details
- Set event capacity
- View registration counts
- Delete events

✅ **QR Code Generation**
- Generate unique QR codes for each event
- College logo embedded in QR codes
- Time-limited QR codes
- Download QR codes as images

✅ **Attendance Tracking**
- Real-time attendance monitoring
- View registered vs. attended students
- Department-wise statistics
- Student-wise attendance reports

✅ **Reporting & Analytics**
- Comprehensive attendance reports
- Event statistics dashboard
- Department-wise analysis
- Export to Excel (.xlsx)

✅ **Security Monitoring**
- Unauthorized scan logs
- Failed authentication attempts
- Suspicious activity tracking

### System Features

✅ **Security**
- JWT token-based authentication (24-hour expiration)
- Password hashing with bcrypt
- Input sanitization and validation
- XSS prevention
- SQL/NoSQL injection protection
- CSRF protection
- Rate limiting (200/day, 50/hour)
- Content Security Policy (production)
- HSTS (production)

✅ **Performance**
- Responsive design (mobile, tablet, desktop)
- Optimized database queries
- Efficient QR code scanning
- Fast data export

✅ **User Experience**
- Clean, modern interface
- Smooth animations
- Intuitive navigation
- Real-time feedback
- Error handling with user-friendly messages

---

## Technology Stack

### Backend

| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.8+ | Core programming language |
| **Flask** | 3.0.0 | Web framework |
| **Flask-CORS** | 4.0.0 | Cross-origin resource sharing |
| **Flask-Limiter** | 3.5.0 | Rate limiting |
| **Flask-Talisman** | 1.1.0 | Security headers |
| **PyMongo** | 4.6.1 | MongoDB driver |
| **MongoDB** | 4.0+ | NoSQL database |
| **PyJWT** | 2.8.0 | JWT token handling |
| **bcrypt** | 4.1.2 | Password hashing |
| **python-dotenv** | 1.0.0 | Environment variables |
| **qrcode** | 7.4.2 | QR code generation |
| **Pillow** | 10.1.0 | Image processing |
| **openpyxl** | 3.1.2 | Excel file generation |
| **validators** | 0.22.0 | Input validation |

### Frontend

| Technology | Purpose |
|------------|---------|
| **HTML5** | Structure |
| **CSS3** | Styling with custom properties |
| **JavaScript (ES6+)** | Client-side logic |
| **ZXing Library** | QR code scanning |
| **Fetch API** | HTTP requests |

### Infrastructure

| Component | Technology |
|-----------|------------|
| **Database** | MongoDB 4.0+ |
| **Server** | Flask Development Server / Gunicorn (production) |
| **OS** | Windows/Linux/macOS |

---

## System Architecture

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend Layer                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  HTML5   │  │   CSS3   │  │JavaScript│  │  ZXing   │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│       │              │              │              │         │
└───────┼──────────────┼──────────────┼──────────────┼─────────┘
        │              │              │              │
        └──────────────┴──────────────┴──────────────┘
                           ▼
        ┌──────────────────────────────────────────┐
        │           API Gateway (Flask)            │
        │  ┌────────────────────────────────────┐ │
        │  │  CORS │ Rate Limiter │ Talisman   │ │
        │  └────────────────────────────────────┘ │
        └──────────────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                      Backend Layer (Flask)                   │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐           │
│  │   Routes   │  │   Models   │  │   Utils    │           │
│  ├────────────┤  ├────────────┤  ├────────────┤           │
│  │ • auth     │  │ • student  │  │ • sanitizer│           │
│  │ • student  │  │ • event    │  │ • validator│           │
│  │ • admin    │  │ • attendance│  │ • qr_gen   │           │
│  │ • attendance│ │ • unauth   │  │ • email    │           │
│  └────────────┘  └────────────┘  └────────────┘           │
└─────────────────────────────────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    Database Layer (MongoDB)                  │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐           │
│  │  students  │  │   events   │  │ attendance │           │
│  └────────────┘  └────────────┘  └────────────┘           │
│  ┌────────────────────────────────────────────┐           │
│  │         unauthorized_scans                  │           │
│  └────────────────────────────────────────────┘           │
└─────────────────────────────────────────────────────────────┘
```

### Component Breakdown

#### Frontend Components

```
frontend/
├── index.html              # Landing page
├── css/
│   └── style.css          # Global styles with animations
├── js/
│   ├── login.js           # Login functionality
│   ├── register.js        # Registration logic
│   ├── events.js          # Student event dashboard
│   ├── admin.js           # Admin dashboard
│   ├── scan.js            # QR scanning page
│   └── utils.js           # Security & utility functions
└── pages/
    ├── login.html         # Student login
    ├── register.html      # Student registration
    ├── events.html        # Student dashboard
    ├── admin_login.html   # Admin login
    ├── admin_dashboard.html # Admin panel
    ├── scan.html          # QR scanner
    └── success.html       # Success confirmation
```

#### Backend Components

```
backend/
├── app.py                 # Flask application setup
├── config.py              # Configuration management
├── models/
│   ├── __init__.py        # MongoDB connection
│   ├── student.py         # Student data model
│   ├── event.py           # Event data model
│   ├── attendance.py      # Attendance records
│   └── unauthorized_log.py # Security logs
├── routes/
│   ├── auth.py            # Authentication endpoints
│   ├── student.py         # Student operations
│   ├── admin.py           # Admin operations
│   └── attendance.py      # Attendance endpoints
└── utils/
    ├── sanitizer.py       # Input sanitization
    ├── validators.py      # Input validation
    ├── qr_generator.py    # QR code generation
    └── email_service.py   # Email notifications
```

### Data Flow

#### Student Registration Flow
```
1. Student → Frontend (register.html)
2. Frontend → POST /api/auth/register
3. Backend → Validate inputs (sanitizer, validator)
4. Backend → Hash password (bcrypt)
5. Backend → Save to MongoDB (students collection)
6. Backend → Generate JWT token
7. Backend → Response with token
8. Frontend → Store token in localStorage
9. Frontend → Redirect to events.html
```

#### Event Registration Flow
```
1. Student → Select event (events.html)
2. Frontend → POST /api/student/register-event
3. Backend → Verify JWT token
4. Backend → Check event capacity
5. Backend → Check duplicate registration
6. Backend → Update student.registered_events (ObjectId)
7. Backend → Increment event.total_registered
8. Backend → Response with success
9. Frontend → Update UI
```

#### QR Code Attendance Flow
```
1. Admin → Generate QR code (admin_dashboard.html)
2. Backend → Create QR data with token
3. Backend → Generate QR image with logo
4. Backend → Return base64 image
5. Admin → Display/Print QR code
6. Student → Scan QR code (events.html or scan.html)
7. Frontend → Decode QR data (ZXing)
8. Frontend → POST /api/attendance/mark
9. Backend → Verify event & student
10. Backend → Check QR token validity
11. Backend → Mark attendance (ObjectId)
12. Backend → Response with success
13. Frontend → Show confirmation
```

---

## Installation & Setup

### Prerequisites

#### Required Software

1. **Python 3.8 or higher**
   ```bash
   # Check Python version
   python --version
   # or
   py --version
   ```

2. **MongoDB 4.0 or higher**
   - Download: https://www.mongodb.com/try/download/community
   - Default connection: `mongodb://localhost:27017/`

3. **Git** (optional, for cloning)
   ```bash
   git --version
   ```

4. **Modern Web Browser**
   - Chrome, Firefox, Edge, or Safari
   - Required for QR code scanning (camera access)

### Step-by-Step Installation

#### 1. Download/Clone the Project

```bash
# If using Git
git clone <repository-url>
cd EMS

# Or download and extract ZIP file
```

#### 2. Navigate to Backend Directory

```bash
cd backend
```

#### 3. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
# or
py -m venv venv
```

**Linux/Mac:**
```bash
python3 -m venv venv
```

#### 4. Activate Virtual Environment

**Windows:**
```bash
.\venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

#### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs all required packages:
- Flask, Flask-CORS, Flask-Limiter, Flask-Talisman
- PyMongo, PyJWT, bcrypt
- qrcode, Pillow, openpyxl, validators

#### 6. Create Environment File

Create a `.env` file in the `backend/` directory:

```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

Edit `.env` file with your configuration:

```env
# Flask Configuration
SECRET_KEY=your-secret-key-here-change-in-production
JWT_SECRET_KEY=your-jwt-secret-key-here

# MongoDB Configuration
MONGO_URI=mongodb://localhost:27017/
DATABASE_NAME=college_ems

# Admin Credentials
ADMIN_EMAIL=admin@college.edu
ADMIN_PASSWORD=Admin@123

# Email Configuration (Optional)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com

# Application Settings
FLASK_ENV=development
FLASK_DEBUG=True
```

#### 7. Start MongoDB

**Windows:**
```bash
# Start MongoDB service
net start MongoDB

# Or run MongoDB manually
"C:\Program Files\MongoDB\Server\4.4\bin\mongod.exe" --dbpath="C:\data\db"
```

**Linux:**
```bash
sudo systemctl start mongod
```

**Mac:**
```bash
brew services start mongodb-community
```

#### 8. Initialize Database (Optional)

The application automatically creates collections and default events on first run. To manually initialize:

```bash
# From backend directory
python
>>> from app import app
>>> from models.event import Event
>>> with app.app_context():
...     Event.initialize_default_events()
>>> exit()
```

#### 9. Start the Application

**Option A: Using start.bat (Windows)**
```bash
# From project root directory
.\start.bat
```

**Option B: Manual Start**
```bash
# From backend directory with venv activated
python app.py
# or
flask run
```

**Option C: Using start-simple.bat**
```bash
# Simplified startup script
.\start-simple.bat
```

#### 10. Access the Application

Open your browser and navigate to:
```
http://localhost:5000
```

You should see the landing page with options for:
- Student Login
- Student Register
- Admin Login

---

## Configuration

### Environment Variables

Edit `backend/.env` file to configure the application:

#### Flask Configuration

```env
SECRET_KEY=your-secret-key-here-change-in-production
```
- Used for Flask session management
- **IMPORTANT:** Change in production to a strong random string
- Generate with: `python -c "import secrets; print(secrets.token_hex(32))"`

```env
JWT_SECRET_KEY=your-jwt-secret-key-here
```
- Used for JWT token signing
- **IMPORTANT:** Change in production to a different strong random string
- Should be different from SECRET_KEY

```env
FLASK_ENV=development
FLASK_DEBUG=True
```
- `development`: Disables Talisman security headers, enables debug mode
- `production`: Enables full security headers, disables debug mode

#### MongoDB Configuration

```env
MONGO_URI=mongodb://localhost:27017/
DATABASE_NAME=college_ems
```
- `MONGO_URI`: MongoDB connection string
- For authenticated MongoDB: `mongodb://username:password@localhost:27017/`
- For MongoDB Atlas: `mongodb+srv://username:password@cluster.mongodb.net/`
- `DATABASE_NAME`: Name of the database (default: college_ems)

#### Admin Credentials

```env
ADMIN_EMAIL=admin@college.edu
ADMIN_PASSWORD=Admin@123
```
- Used for admin login
- **IMPORTANT:** Change ADMIN_PASSWORD in production
- Password requirements: min 8 chars, uppercase, lowercase, number, special char

#### Email Configuration (Optional)

```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com
```

**Gmail Setup:**
1. Enable 2-Step Verification in Google Account
2. Go to Security → App passwords
3. Generate app password for "Mail" on "Windows Computer"
4. Use the 16-character code (no spaces) as MAIL_PASSWORD

**Note:** Email is OPTIONAL. The system works without email configuration.

### Application Configuration

Edit `backend/config.py` for advanced settings:

```python
# JWT Token Expiration
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)  # Change as needed

# Rate Limiting
RATELIMIT_STORAGE_URL = 'memory://'  # Use Redis in production
# Default limits: 200 per day, 50 per hour

# CORS Origins
# In app.py, change to specific domains in production:
# CORS(app, resources={r"/api/*": {"origins": "https://yourdomain.com"}})
```

---

## Running the Application

### Development Mode

#### Quick Start (Windows)

```bash
# From project root
.\start.bat
```

This script:
1. Checks MongoDB is running
2. Activates virtual environment
3. Starts Flask application
4. Opens browser to http://localhost:5000

#### Manual Start

```bash
# 1. Start MongoDB
net start MongoDB

# 2. Navigate to backend
cd backend

# 3. Activate virtual environment
.\venv\Scripts\activate

# 4. Run Flask
python app.py
```

#### Alternative: Flask CLI

```bash
# From backend directory with venv activated
set FLASK_APP=app.py
set FLASK_ENV=development
flask run

# Linux/Mac
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

### Production Mode

#### 1. Update Configuration

Edit `backend/.env`:
```env
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=<strong-random-key>
JWT_SECRET_KEY=<strong-random-key>
ADMIN_PASSWORD=<strong-password>
```

#### 2. Use Production Server (Gunicorn)

Install Gunicorn:
```bash
pip install gunicorn
```

Run with Gunicorn:
```bash
# From backend directory
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

- `-w 4`: 4 worker processes
- `-b 0.0.0.0:8000`: Bind to all interfaces on port 8000

#### 3. Use Nginx as Reverse Proxy

Nginx configuration example:
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static {
        alias /path/to/EMS/frontend;
    }
}
```

### Stopping the Application

**Stop Flask (Ctrl+C in terminal)**

**Stop using stop.bat:**
```bash
.\stop.bat
```

**Stop MongoDB:**
```bash
net stop MongoDB
```

---

## User Guide

### For Students

#### 1. Registration

**URL:** http://localhost:5000/pages/register.html

**Steps:**
1. Click "Student Register" on the landing page
2. Fill in the registration form:
   - Name (full name)
   - Email (college email)
   - Phone Number (10 digits)
   - Register Number (student ID)
   - Department (select from dropdown)
   - Course/Programme (select based on department)
   - Year (1st, 2nd, 3rd, 4th)
   - Password (min 8 chars, must include uppercase, lowercase, number, special char)
3. Click "Register"
4. On success, automatically logged in and redirected to Events page

**Validation Rules:**
- Email: Must be valid format, unique
- Phone: 10 digits only
- Register Number: Alphanumeric, unique
- Password: Min 8 chars, 1 uppercase, 1 lowercase, 1 number, 1 special char

#### 2. Login

**URL:** http://localhost:5000/pages/login.html

**Steps:**
1. Click "Student Login" on the landing page
2. Enter email and password
3. Click "Login"
4. Redirected to Events dashboard

**Features:**
- JWT token stored in localStorage
- Token valid for 24 hours
- Auto-logout on token expiration

#### 3. Browse & Register for Events

**URL:** http://localhost:5000/pages/events.html (after login)

**View Events:**
- All available events displayed as cards
- Each card shows:
  - Event name
  - Description
  - Date
  - Venue
  - Capacity
  - Registration count

**Register for Event:**
1. Click on event card (radio button selected)
2. Click "Register for Selected Event"
3. See confirmation message
4. Event added to "My Registrations"

**Features:**
- Can register for multiple events
- Cannot register for same event twice
- Cannot register if event is full
- Real-time capacity updates

#### 4. View Profile

**In Events Dashboard:**
1. Click "My Profile" button
2. View your information:
   - Name
   - Register Number
   - Department
   - Course
   - Year
   - Email
   - Registered Events count

#### 5. Mark Attendance with QR Code

**Method 1: In Events Dashboard**
1. Click "Scan QR" button
2. Allow camera access
3. Point camera at event QR code
4. Automatic scan and attendance marking
5. See confirmation message

**Method 2: Dedicated Scan Page**
1. Go to http://localhost:5000/pages/scan.html
2. Login if not already logged in
3. Click "Start Scanning"
4. Allow camera access
5. Scan QR code
6. See attendance confirmation

**Features:**
- Instant attendance marking
- Duplicate scan prevention
- Unauthorized scan detection
- Attendance history view

#### 6. View Attendance History

**In Scan Page:**
- Scroll down to "My Attendance Records"
- See all events you've attended:
  - Event name
  - Date attended
  - Status (Present)

#### 7. Logout

Click "Logout" button in any dashboard to:
- Clear authentication token
- Return to login page

---

## Admin Guide

### Admin Login

**URL:** http://localhost:5000/pages/admin_login.html

**Default Credentials:**
- Email: `admin@college.edu`
- Password: `Admin@123`

**Steps:**
1. Click "Admin Login" on landing page
2. Enter admin email and password
3. Click "Login"
4. Redirected to Admin Dashboard

### Admin Dashboard Overview

**URL:** http://localhost:5000/pages/admin_dashboard.html (after login)

**Dashboard Sections:**
1. **Statistics Panel**
   - Total Events
   - Total Students
   - Today's Attendance
   - Recent Activity

2. **Tabs:**
   - Events (default)
   - QR Codes
   - Attendance Report
   - All Students

### Managing Events

#### View All Events

**Events Tab:**
- Lists all events with details
- Shows registration count
- Action buttons for each event

#### Create New Event

**Steps:**
1. Click "Events" tab
2. Fill in the form:
   - Event Name
   - Description
   - Date (YYYY-MM-DD)
   - Venue
   - Max Participants
3. Click "Create Event"
4. Event appears in the list

**Validation:**
- All fields required except Max Participants
- Date must be valid format

#### Edit Event

**Steps:**
1. Find event in the list
2. Update fields directly in the form
3. Click "Update Event"
4. Changes saved immediately

#### Delete Event

**Steps:**
1. Find event in the list
2. Click "Delete" button
3. Event removed (WARNING: No confirmation dialog)

**Note:** Deleting an event doesn't remove attendance records.

### Generate QR Codes

**QR Codes Tab:**

#### Generate QR Code for Event

**Steps:**
1. Click "QR Codes" tab
2. Select event from dropdown
3. Click "Generate QR Code"
4. QR code displayed with college logo

**Features:**
- College logo embedded in center
- High error correction (ERROR_CORRECT_H)
- Unique token for each QR code
- Base64 encoded image

#### Download QR Code

**Steps:**
1. Generate QR code (see above)
2. Right-click on QR code image
3. Select "Save image as..."
4. Save as PNG file

**Note:** QR code includes event ID and security token

#### Print QR Code

**Steps:**
1. Generate QR code
2. Click browser's print button (Ctrl+P)
3. Select "Print selection" or adjust print area
4. Print on paper or save as PDF

**Tips:**
- Print in high quality for better scanning
- Ensure QR code is at least 2x2 inches
- Test scanning before event

### Attendance Reports

**Attendance Report Tab:**

#### Generate Attendance Report

**Steps:**
1. Click "Attendance Report" tab
2. Select event from dropdown
3. Click "Generate Report"
4. Report displayed with statistics

**Report Includes:**
- Event name and details
- Total Registered students
- Total Attended students
- Absent count
- Attendance percentage

**Student Lists:**
- **Registered Students:** All who registered
  - Name, Register Number, Department, Year
  - Attendance Status (Present/Absent in green/red)
- **Absent Students:** Those who didn't attend
  - Name, Register Number, Department, Year

#### Export to Excel

**Steps:**
1. Generate attendance report (see above)
2. Click "Export to Excel" button
3. Excel file (.xlsx) downloaded automatically

**Excel Contents:**
- Sheet 1: Summary
  - Event details
  - Total counts
  - Percentage
- Sheet 2: Registered Students
  - Complete list with status
- Sheet 3: Absent Students
  - List of absent students

**Filename Format:** `attendance_<EventName>_<Date>.xlsx`

### View All Students

**All Students Tab:**

**Features:**
- Lists all registered students
- Shows:
  - Name
  - Register Number
  - Email
  - Department
  - Year
  - Number of events registered
- Search functionality (if implemented)

### Department Statistics

**Stats Section (if implemented):**
- View registrations by department
- See most active departments
- Analyze participation trends

### Unauthorized Scan Logs

**Security Monitoring:**

To view unauthorized scans (students scanning without registration):
- Currently requires database query
- Future feature: Add to dashboard

**Query MongoDB:**
```javascript
use college_ems
db.unauthorized_scans.find().pretty()
```

### Admin Best Practices

1. **Regular Backups:**
   - Export attendance after each event
   - Backup database weekly

2. **QR Code Security:**
   - Generate QR codes just before event
   - Don't share QR codes publicly
   - Use time-limited QR codes

3. **Monitor Attendance:**
   - Check attendance reports after events
   - Verify counts match expectations
   - Investigate anomalies

4. **Student Management:**
   - Review student registrations regularly
   - Remove duplicate accounts
   - Update student information as needed

5. **Event Planning:**
   - Set realistic capacity limits
   - Create events well in advance
   - Update event details if venue/date changes

---

## API Documentation

### Base URL

```
http://localhost:5000/api
```

### Authentication

Most endpoints require JWT token in Authorization header:

```http
Authorization: Bearer <token>
```

Token obtained from login/register endpoints, valid for 24 hours.

---

### Authentication Endpoints

#### 1. Student Registration

**POST** `/api/auth/register`

**Request Body:**
```json
{
  "name": "SANJAYKUMAR M",
  "email": "sanjay@college.edu",
  "phone": "9876543210",
  "register_number": "927623BCS096",
  "department": "Computer Science",
  "course": "B.E. Computer Science",
  "year": "3rd Year",
  "password": "Sanjay@123"
}
```

**Response (Success):**
```json
{
  "success": true,
  "message": "Registration successful",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "student_id": "65a5b87ed7fc256cc0914deb"
}
```

**Response (Error):**
```json
{
  "success": false,
  "message": "Email already registered"
}
```

**Status Codes:**
- 201: Created
- 400: Validation error
- 409: Email/Register number already exists
- 500: Server error

---

#### 2. Student Login

**POST** `/api/auth/login`

**Request Body:**
```json
{
  "email": "sanjay@college.edu",
  "password": "Sanjay@123"
}
```

**Response (Success):**
```json
{
  "success": true,
  "message": "Login successful",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "student_id": "65a5b87ed7fc256cc0914deb"
}
```

**Response (Error):**
```json
{
  "success": false,
  "message": "Invalid email or password"
}
```

**Status Codes:**
- 200: Success
- 401: Invalid credentials
- 500: Server error

---

#### 3. Admin Login

**POST** `/api/auth/admin-login`

**Request Body:**
```json
{
  "email": "admin@college.edu",
  "password": "Admin@123"
}
```

**Response (Success):**
```json
{
  "success": true,
  "message": "Admin login successful",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "role": "admin"
}
```

**Status Codes:**
- 200: Success
- 401: Invalid credentials
- 500: Server error

---

#### 4. Verify Token

**GET** `/api/auth/verify`

**Headers:**
```
Authorization: Bearer <token>
```

**Response (Success):**
```json
{
  "success": true,
  "valid": true,
  "student_id": "65a5b87ed7fc256cc0914deb"
}
```

**Response (Expired):**
```json
{
  "success": false,
  "message": "Token has expired"
}
```

**Status Codes:**
- 200: Valid token
- 401: Invalid/Expired token

---

### Student Endpoints

#### 5. Get All Events

**GET** `/api/student/events`

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "success": true,
  "events": [
    {
      "id": "65a5b87ed7fc256cc0914dec",
      "event_name": "Paper Presentation",
      "description": "Present your research and technical papers",
      "date": "2026-03-15",
      "venue": "Main Auditorium",
      "max_participants": 100,
      "total_registered": 25
    },
    ...
  ]
}
```

**Status Codes:**
- 200: Success
- 401: Unauthorized
- 500: Server error

---

#### 6. Register for Event

**POST** `/api/student/register-event`

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "event_id": "65a5b87ed7fc256cc0914dec"
}
```

**Response (Success):**
```json
{
  "success": true,
  "message": "Successfully registered for event"
}
```

**Response (Already Registered):**
```json
{
  "success": false,
  "message": "You are already registered for this event"
}
```

**Response (Full):**
```json
{
  "success": false,
  "message": "Event is full. Maximum participants reached."
}
```

**Status Codes:**
- 200: Success
- 400: Already registered / Event full
- 401: Unauthorized
- 404: Event not found
- 500: Server error

---

#### 7. Get Student Profile

**GET** `/api/student/profile`

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "success": true,
  "student": {
    "id": "65a5b87ed7fc256cc0914deb",
    "name": "SANJAYKUMAR M",
    "email": "sanjay@college.edu",
    "phone": "9876543210",
    "register_number": "927623BCS096",
    "department": "Computer Science",
    "course": "B.E. Computer Science",
    "year": "3rd Year",
    "registered_events": [
      "65a5b87ed7fc256cc0914dec"
    ],
    "created_at": "2024-01-15T10:30:00"
  }
}
```

**Status Codes:**
- 200: Success
- 401: Unauthorized
- 404: Student not found
- 500: Server error

---

#### 8. Check Registration Status

**GET** `/api/student/check-registration/<event_id>`

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "success": true,
  "registered": true,
  "attended": false
}
```

**Status Codes:**
- 200: Success
- 401: Unauthorized
- 500: Server error

---

#### 9. Get Student Attendance

**GET** `/api/student/my-attendance`

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "success": true,
  "attendance": [
    {
      "event_name": "Paper Presentation",
      "event_date": "2026-03-15",
      "venue": "Main Auditorium",
      "attended_at": "2026-03-15T09:30:00"
    },
    ...
  ]
}
```

**Status Codes:**
- 200: Success
- 401: Unauthorized
- 500: Server error

---

### Admin Endpoints

#### 10. Create Event

**POST** `/api/admin/events`

**Headers:**
```
Authorization: Bearer <admin-token>
```

**Request Body:**
```json
{
  "event_name": "Hackathon 2026",
  "description": "24-hour coding competition",
  "date": "2026-04-20",
  "venue": "Innovation Lab",
  "max_participants": 50
}
```

**Response:**
```json
{
  "success": true,
  "message": "Event created successfully",
  "event_id": "65a5b88ed7fc256cc0914ded"
}
```

**Status Codes:**
- 201: Created
- 400: Validation error
- 401: Unauthorized
- 500: Server error

---

#### 11. Get All Events (Admin)

**GET** `/api/admin/events`

**Headers:**
```
Authorization: Bearer <admin-token>
```

**Response:**
```json
{
  "success": true,
  "events": [
    {
      "id": "65a5b87ed7fc256cc0914dec",
      "event_name": "Paper Presentation",
      "description": "Present your research",
      "date": "2026-03-15",
      "venue": "Main Auditorium",
      "max_participants": 100,
      "total_registered": 25,
      "created_at": "2024-01-01T00:00:00"
    },
    ...
  ]
}
```

**Status Codes:**
- 200: Success
- 401: Unauthorized
- 500: Server error

---

#### 12. Update Event

**PUT** `/api/admin/events/<event_id>`

**Headers:**
```
Authorization: Bearer <admin-token>
```

**Request Body:**
```json
{
  "event_name": "Updated Name",
  "description": "Updated description",
  "date": "2026-04-25",
  "venue": "New Venue",
  "max_participants": 75
}
```

**Response:**
```json
{
  "success": true,
  "message": "Event updated successfully"
}
```

**Status Codes:**
- 200: Success
- 400: Validation error
- 401: Unauthorized
- 404: Event not found
- 500: Server error

---

#### 13. Delete Event

**DELETE** `/api/admin/events/<event_id>`

**Headers:**
```
Authorization: Bearer <admin-token>
```

**Response:**
```json
{
  "success": true,
  "message": "Event deleted successfully"
}
```

**Status Codes:**
- 200: Success
- 401: Unauthorized
- 404: Event not found
- 500: Server error

---

#### 14. Generate QR Code

**POST** `/api/admin/generate-qr`

**Headers:**
```
Authorization: Bearer <admin-token>
```

**Request Body:**
```json
{
  "event_id": "65a5b87ed7fc256cc0914dec"
}
```

**Response:**
```json
{
  "success": true,
  "qr_code": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUg...",
  "event_name": "Paper Presentation"
}
```

**Status Codes:**
- 200: Success
- 401: Unauthorized
- 404: Event not found
- 500: Server error

---

#### 15. Get All Students

**GET** `/api/admin/students`

**Headers:**
```
Authorization: Bearer <admin-token>
```

**Response:**
```json
{
  "success": true,
  "students": [
    {
      "id": "65a5b87ed7fc256cc0914deb",
      "name": "SANJAYKUMAR M",
      "email": "sanjay@college.edu",
      "register_number": "927623BCS096",
      "department": "Computer Science",
      "year": "3rd Year",
      "registered_events_count": 3
    },
    ...
  ]
}
```

**Status Codes:**
- 200: Success
- 401: Unauthorized
- 500: Server error

---

#### 16. Get Event Statistics

**GET** `/api/admin/stats`

**Headers:**
```
Authorization: Bearer <admin-token>
```

**Response:**
```json
{
  "success": true,
  "stats": {
    "total_events": 5,
    "total_students": 150,
    "total_registrations": 425,
    "today_attendance": 45
  }
}
```

**Status Codes:**
- 200: Success
- 401: Unauthorized
- 500: Server error

---

### Attendance Endpoints

#### 17. Mark Attendance

**POST** `/api/attendance/mark`

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "event_id": "65a5b87ed7fc256cc0914dec",
  "qr_token": "abc123xyz789"
}
```

**Response (Success):**
```json
{
  "success": true,
  "message": "Attendance marked successfully",
  "event_name": "Paper Presentation"
}
```

**Response (Not Registered):**
```json
{
  "success": false,
  "message": "You are not registered for this event",
  "unauthorized": true
}
```

**Response (Already Marked):**
```json
{
  "success": false,
  "message": "Attendance already marked for this event"
}
```

**Status Codes:**
- 200: Success
- 400: Already marked
- 401: Unauthorized/Not registered
- 404: Event not found
- 500: Server error

---

#### 18. Get Attendance Report

**GET** `/api/attendance/report/<event_id>`

**Headers:**
```
Authorization: Bearer <admin-token>
```

**Response:**
```json
{
  "success": true,
  "event": {
    "id": "65a5b87ed7fc256cc0914dec",
    "event_name": "Paper Presentation",
    "date": "2026-03-15",
    "venue": "Main Auditorium"
  },
  "statistics": {
    "total_registered": 25,
    "total_attended": 20,
    "total_absent": 5,
    "attendance_percentage": 80.0
  },
  "registered_students": [
    {
      "name": "SANJAYKUMAR M",
      "register_number": "927623BCS096",
      "department": "Computer Science",
      "year": "3rd Year",
      "attended": true,
      "attended_at": "2026-03-15T09:30:00"
    },
    ...
  ],
  "absent_students": [
    {
      "name": "Student Name",
      "register_number": "REG123",
      "department": "IT",
      "year": "2nd Year"
    },
    ...
  ]
}
```

**Status Codes:**
- 200: Success
- 401: Unauthorized
- 404: Event not found
- 500: Server error

---

#### 19. Export Attendance to Excel

**GET** `/api/attendance/export/<event_id>`

**Headers:**
```
Authorization: Bearer <admin-token>
```

**Response:**
- Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
- Content-Disposition: attachment; filename="attendance_<EventName>_<Date>.xlsx"
- Binary Excel file

**Status Codes:**
- 200: Success (file download)
- 401: Unauthorized
- 404: Event not found
- 500: Server error

---

#### 20. Get Department Statistics

**GET** `/api/attendance/department-stats/<event_id>`

**Headers:**
```
Authorization: Bearer <admin-token>
```

**Response:**
```json
{
  "success": true,
  "department_stats": [
    {
      "department": "Computer Science",
      "registered": 45,
      "attended": 40,
      "percentage": 88.9
    },
    {
      "department": "Information Technology",
      "registered": 38,
      "attended": 35,
      "percentage": 92.1
    },
    ...
  ]
}
```

**Status Codes:**
- 200: Success
- 401: Unauthorized
- 404: Event not found
- 500: Server error

---

### Utility Endpoints

#### 21. Health Check

**GET** `/api/health`

**No authentication required**

**Response:**
```json
{
  "status": "healthy",
  "message": "College EMS API is running"
}
```

**Status Codes:**
- 200: Success

---

### Error Response Format

All error responses follow this format:

```json
{
  "success": false,
  "message": "Error description"
}
```

### Rate Limiting

Default limits (configurable in config.py):
- **200 requests per day** per IP
- **50 requests per hour** per IP

**Rate Limit Exceeded Response:**
```json
{
  "success": false,
  "message": "Rate limit exceeded. Please try again later."
}
```

**Status Code:** 429 Too Many Requests

---

## Security Features

### 1. Authentication & Authorization

#### JWT Tokens
- **Algorithm:** HS256
- **Expiration:** 24 hours
- **Payload:** `student_id`, `email`, `iat`, `exp`
- **Storage:** localStorage (client-side)

**Token Structure:**
```
Header.Payload.Signature
```

**Security Measures:**
- Tokens signed with JWT_SECRET_KEY
- Automatic expiration after 24 hours
- Token verification on protected routes
- Separate admin authentication

#### Password Security
- **Hashing:** bcrypt with salt rounds
- **Storage:** Never stored in plain text
- **Requirements:** 
  - Minimum 8 characters
  - At least 1 uppercase letter
  - At least 1 lowercase letter
  - At least 1 number
  - At least 1 special character

**Password Hashing:**
```python
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
```

### 2. Input Validation & Sanitization

#### InputSanitizer Class

Located in `backend/utils/sanitizer.py`:

**Methods:**
1. `sanitize_string(value)` - Remove HTML/script tags
2. `sanitize_email(email)` - Email format validation
3. `sanitize_register_number(reg_no)` - Alphanumeric only
4. `sanitize_phone(phone)` - 10-digit validation
5. `sanitize_name(name)` - Allow letters, spaces, dots
6. `sanitize_search_query(query)` - Remove special chars
7. `validate_object_id(obj_id)` - MongoDB ObjectId validation
8. `sanitize_dict(data, fields)` - Bulk sanitization

**XSS Prevention:**
```python
def sanitize_string(self, value):
    if not value:
        return value
    # Remove HTML tags
    value = re.sub(r'<[^>]*>', '', value)
    # Escape special characters
    value = html.escape(value)
    return value.strip()
```

#### Validators Class

Located in `backend/utils/validators.py`:

**Methods:**
1. `validate_email(email)` - RFC-compliant email validation
2. `validate_phone(phone)` - Indian phone number format
3. `validate_register_number(reg_no)` - Alphanumeric 5-15 chars
4. `validate_password(password)` - Strength requirements
5. `validate_date(date_string)` - YYYY-MM-DD format

**Applied On:**
- All registration endpoints
- Login endpoints
- Event creation/update
- QR code generation
- Database queries

### 3. HTTP Security Headers

#### Flask-Talisman (Production Only)

Applied when `FLASK_ENV=production`:

**Headers:**
- **Content-Security-Policy (CSP):**
  ```
  default-src 'self';
  script-src 'self' 'unsafe-inline' 'unsafe-eval' cdn.jsdelivr.net unpkg.com;
  style-src 'self' 'unsafe-inline' fonts.googleapis.com cdnjs.cloudflare.com;
  font-src 'self' fonts.gstatic.com cdnjs.cloudflare.com;
  img-src 'self' data: blob:;
  connect-src 'self';
  ```

- **Strict-Transport-Security (HSTS):**
  ```
  max-age=31536000; includeSubDomains
  ```

- **X-Frame-Options:**
  ```
  DENY
  ```

- **Referrer-Policy:**
  ```
  strict-origin-when-cross-origin
  ```

- **Feature-Policy:**
  ```
  geolocation 'none';
  camera 'self';
  microphone 'none';
  ```

**Development Mode:**
Talisman disabled to avoid CSP/HTTPS issues:
```python
if os.getenv('FLASK_ENV') == 'production':
    Talisman(app, ...)
else:
    logging.info("Development mode - Talisman security headers disabled")
```

### 4. Rate Limiting

#### Flask-Limiter

**Configuration:**
```python
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    storage_uri='memory://',  # Use Redis in production
    default_limits=["200 per day", "50 per hour"]
)
```

**Custom Limits:**
- Login endpoints: Stricter limits (coming soon)
- Registration: IP-based throttling
- Admin operations: Higher limits

**Headers Sent:**
```
X-RateLimit-Limit: 200
X-RateLimit-Remaining: 199
X-RateLimit-Reset: 1709481600
```

### 5. CORS Policy

**Current Configuration:**
```python
CORS(app, resources={r"/api/*": {"origins": "*"}})
```

**Production Recommendation:**
```python
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://yourdomain.com"],
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
```

### 6. Database Security

#### MongoDB Security

**NoSQL Injection Prevention:**
- All queries use PyMongo dictionaries
- ObjectId validation before queries
- No string concatenation in queries

**Safe Query Example:**
```python
# SAFE
student = collection.find_one({'_id': ObjectId(student_id)})

# UNSAFE (NOT USED)
# student = collection.find_one({"$where": user_input})
```

**Data Type Validation:**
- ObjectId conversion: `ObjectId(id)` with try-except
- Type checking before database operations
- Backward-compatible queries with `$or`

#### Connection Security

**Development:**
```
mongodb://localhost:27017/
```

**Production (Recommended):**
```
mongodb://username:password@localhost:27017/dbname?authSource=admin
```

**MongoDB Atlas:**
```
mongodb+srv://username:password@cluster.mongodb.net/dbname?retryWrites=true&w=majority
```

### 7. QR Code Security

#### Unique Tokens
```python
qr_token = secrets.token_urlsafe(32)  # Cryptographically secure
```

**QR Data Structure:**
```json
{
  "event_id": "65a5b87ed7fc256cc0914dec",
  "qr_token": "abc123xyz789...",
  "generated_at": "2026-03-15T08:00:00"
}
```

**Security Measures:**
- Unique token per QR generation
- Event ID validation
- Registration verification
- Duplicate scan prevention
- Unauthorized scan logging

#### Unauthorized Scan Logging

When student scans QR without registration:
```python
UnauthorizedLog.create(
    student_id=student_id,
    event_id=event_id,
    scanned_at=datetime.utcnow()
)
```

### 8. Error Handling

**Principle:** Never expose sensitive information in errors

**Bad Practice (NOT USED):**
```python
except Exception as e:
    return jsonify({'error': str(e)}), 500  # Exposes stack trace
```

**Good Practice (USED):**
```python
except Exception as e:
    logger.error(f"Error: {str(e)}")  # Log internally
    return jsonify({'success': False, 'message': 'Internal server error'}), 500
```

**Specific Error Handling:**
```python
except jwt.ExpiredSignatureError:
    return jsonify({'success': False, 'message': 'Token has expired'}), 401
except jwt.InvalidTokenError:
    return jsonify({'success': False, 'message': 'Invalid token'}), 401
```

### 9. Frontend Security

#### XSS Prevention

**utils.js - escapeHtml():**
```javascript
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#x27;',
        '/': '&#x2F;'
    };
    return text.replace(/[&<>"'/]/g, char => map[char]);
}
```

**Usage:**
```javascript
// Before inserting user data into DOM
element.innerHTML = escapeHtml(userData);
```

#### Token Security

**Storage:**
- Stored in localStorage (acceptable for demo)
- Never logged or exposed
- Cleared on logout

**CSRF Protection:**
- SameSite cookies (future enhancement)
- Token validation on each request

**Recommendations for Production:**
- Use httpOnly cookies
- Implement refresh tokens
- Add token rotation

### 10. Logging & Monitoring

**Logging Configuration:**
```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

**What's Logged:**
- Application startup/shutdown
- Authentication attempts
- Error occurrences
- Rate limit violations
- Unauthorized scans

**What's NOT Logged:**
- Passwords (plain or hashed)
- JWT tokens
- Sensitive user data

**Production Recommendations:**
- Use structured logging (JSON)
- Implement log rotation
- Send logs to monitoring service (e.g., ELK stack)
- Set up alerts for security events

### 11. Security Checklist for Production

#### Critical (Must Do)

- [ ] Change SECRET_KEY to strong random value
- [ ] Change JWT_SECRET_KEY to different strong value
- [ ] Change ADMIN_PASSWORD to strong password
- [ ] Set FLASK_ENV=production
- [ ] Set FLASK_DEBUG=False
- [ ] Enable MongoDB authentication
- [ ] Configure SSL/TLS certificates (HTTPS)
- [ ] Tighten CORS policy (specific origins)
- [ ] Use httpOnly cookies for tokens
- [ ] Enable MongoDB replica set with authentication

#### Recommended

- [ ] Use Redis for rate limiting storage
- [ ] Implement refresh token mechanism
- [ ] Add token blacklisting on logout
- [ ] Set up Web Application Firewall (WAF)
- [ ] Enable MongoDB encryption at rest
- [ ] Implement audit logging
- [ ] Add IP whitelisting for admin
- [ ] Set up intrusion detection
- [ ] Regular security audits
- [ ] Dependency vulnerability scanning

#### Monitoring

- [ ] Set up monitoring service (e.g., Prometheus)
- [ ] Configure alerting (e.g., AlertManager)
- [ ] Log aggregation (e.g., ELK stack)
- [ ] Error tracking (e.g., Sentry)
- [ ] Performance monitoring (e.g., New Relic)

---

## Database Schema

### Database Name
```
college_ems
```

### Collections

#### 1. students

**Purpose:** Store student information and registrations

**Schema:**
```javascript
{
  _id: ObjectId,                    // Auto-generated
  name: String,                     // Full name
  email: String,                    // Unique email
  phone: String,                    // 10-digit phone
  register_number: String,          // Unique student ID
  department: String,               // Department name
  course: String,                   // Course/Programme
  year: String,                     // Academic year
  password: String,                 // Bcrypt hashed
  registered_events: [ObjectId],    // Array of event IDs
  created_at: ISODate,              // Registration timestamp
  updated_at: ISODate               // Last update timestamp
}
```

**Indexes:**
```javascript
db.students.createIndex({ email: 1 }, { unique: true })
db.students.createIndex({ register_number: 1 }, { unique: true })
db.students.createIndex({ department: 1 })
```

**Example Document:**
```javascript
{
  "_id": ObjectId("65a5b87ed7fc256cc0914deb"),
  "name": "SANJAYKUMAR M",
  "email": "sanjay@college.edu",
  "phone": "9876543210",
  "register_number": "927623BCS096",
  "department": "Computer Science",
  "course": "B.E. Computer Science",
  "year": "3rd Year",
  "password": "$2b$10$abcdefghijklmnopqrstuvwxyz123456789",
  "registered_events": [
    ObjectId("69a5b87ed7fc256cc0914dec"),
    ObjectId("69a5b87ed7fc256cc0914ded")
  ],
  "created_at": ISODate("2024-01-15T10:30:00Z"),
  "updated_at": ISODate("2024-01-20T14:45:00Z")
}
```

---

#### 2. events

**Purpose:** Store event information

**Schema:**
```javascript
{
  _id: ObjectId,                    // Auto-generated
  event_name: String,               // Event name
  description: String,              // Event description
  date: String,                     // Event date (YYYY-MM-DD)
  venue: String,                    // Venue name
  max_participants: Number,         // Maximum capacity (optional)
  total_registered: Number,         // Count of registrations
  created_at: ISODate,              // Creation timestamp
  updated_at: ISODate               // Last update timestamp
}
```

**Indexes:**
```javascript
db.events.createIndex({ date: 1 })
db.events.createIndex({ event_name: 1 })
```

**Example Document:**
```javascript
{
  "_id": ObjectId("69a5b87ed7fc256cc0914dec"),
  "event_name": "Paper Presentation",
  "description": "Present your research and technical papers",
  "date": "2026-03-15",
  "venue": "Main Auditorium",
  "max_participants": 100,
  "total_registered": 25,
  "created_at": ISODate("2024-01-01T00:00:00Z"),
  "updated_at": ISODate("2024-02-01T12:00:00Z")
}
```

---

#### 3. attendance

**Purpose:** Track student attendance at events

**Schema:**
```javascript
{
  _id: ObjectId,                    // Auto-generated
  student_id: ObjectId,             // Reference to students._id
  event_id: ObjectId,               // Reference to events._id
  attended_at: ISODate,             // Attendance timestamp
  created_at: ISODate               // Record creation timestamp
}
```

**Indexes:**
```javascript
db.attendance.createIndex({ student_id: 1, event_id: 1 }, { unique: true })
db.attendance.createIndex({ event_id: 1 })
db.attendance.createIndex({ attended_at: 1 })
```

**Example Document:**
```javascript
{
  "_id": ObjectId("65b5c97fd8gc367dd1025efc"),
  "student_id": ObjectId("65a5b87ed7fc256cc0914deb"),
  "event_id": ObjectId("69a5b87ed7fc256cc0914dec"),
  "attended_at": ISODate("2026-03-15T09:30:00Z"),
  "created_at": ISODate("2026-03-15T09:30:00Z")
}
```

**Constraints:**
- Composite unique index prevents duplicate attendance
- Cannot mark attendance twice for same event

---

#### 4. unauthorized_scans

**Purpose:** Log unauthorized QR code scans (security monitoring)

**Schema:**
```javascript
{
  _id: ObjectId,                    // Auto-generated
  student_id: ObjectId,             // Student who scanned
  event_id: ObjectId,               // Event they tried to attend
  scanned_at: ISODate,              // Scan timestamp
  reason: String                    // Reason for rejection (optional)
}
```

**Indexes:**
```javascript
db.unauthorized_scans.createIndex({ student_id: 1 })
db.unauthorized_scans.createIndex({ event_id: 1 })
db.unauthorized_scans.createIndex({ scanned_at: 1 })
```

**Example Document:**
```javascript
{
  "_id": ObjectId("65c6da80e9hd478ee2136fgd"),
  "student_id": ObjectId("65a5b87ed7fc256cc0914deb"),
  "event_id": ObjectId("69a5b87ed7fc256cc0914dee"),
  "scanned_at": ISODate("2026-03-16T10:15:00Z"),
  "reason": "Not registered for this event"
}
```

---

### Relationships

```
students (1) ----< (N) registered_events [Array of ObjectIds]
students (1) ----< (N) attendance
events   (1) ----< (N) attendance
students (1) ----< (N) unauthorized_scans
events   (1) ----< (N) unauthorized_scans
```

**Diagram:**
```
┌─────────────┐         ┌─────────────┐
│  students   │         │   events    │
│             │         │             │
│ _id (PK)    │         │ _id (PK)    │
│ email       │         │ event_name  │
│ name        │         │ description │
│ registered_ │         │ date        │
│  events[]   │────────>│ venue       │
└─────────────┘         │ total_reg   │
      │                 └─────────────┘
      │                       │
      │    ┌──────────────────┘
      │    │
      ▼    ▼
┌─────────────┐
│ attendance  │
│             │
│ _id (PK)    │
│ student_id  │──┐
│ event_id    │──┘
│ attended_at │
└─────────────┘
```

---

### Database Operations

#### Initialize Database

```javascript
// Connect to MongoDB
use college_ems

// Create collections (auto-created on first insert)
db.createCollection("students")
db.createCollection("events")
db.createCollection("attendance")
db.createCollection("unauthorized_scans")

// Create indexes
db.students.createIndex({ email: 1 }, { unique: true })
db.students.createIndex({ register_number: 1 }, { unique: true })
db.events.createIndex({ date: 1 })
db.attendance.createIndex({ student_id: 1, event_id: 1 }, { unique: true })
```

#### Common Queries

**Find student by email:**
```javascript
db.students.findOne({ email: "sanjay@college.edu" })
```

**Get all events:**
```javascript
db.events.find().sort({ date: 1 })
```

**Get students registered for event:**
```javascript
db.students.find({
  registered_events: ObjectId("69a5b87ed7fc256cc0914dec")
})
```

**Get attendance for event:**
```javascript
db.attendance.find({
  event_id: ObjectId("69a5b87ed7fc256cc0914dec")
}).count()
```

**Get student's attendance history:**
```javascript
db.attendance.aggregate([
  { $match: { student_id: ObjectId("65a5b87ed7fc256cc0914deb") } },
  { $lookup: {
      from: "events",
      localField: "event_id",
      foreignField: "_id",
      as: "event"
  }},
  { $unwind: "$event" },
  { $sort: { attended_at: -1 } }
])
```

**Get department-wise statistics:**
```javascript
db.students.aggregate([
  { $group: {
      _id: "$department",
      total_students: { $sum: 1 },
      total_registrations: { $sum: { $size: "$registered_events" } }
  }},
  { $sort: { total_students: -1 } }
])
```

---

### Backup & Restore

#### Backup Database

```bash
# Backup entire database
mongodump --db college_ems --out ./backup

# Backup specific collection
mongodump --db college_ems --collection students --out ./backup
```

#### Restore Database

```bash
# Restore entire database
mongorestore --db college_ems ./backup/college_ems

# Restore specific collection
mongorestore --db college_ems --collection students ./backup/college_ems/students.bson
```

#### Export to JSON

```bash
# Export collection to JSON
mongoexport --db college_ems --collection students --out students.json --pretty

# Export with query
mongoexport --db college_ems --collection students --query '{"department":"Computer Science"}' --out cs_students.json
```

#### Import from JSON

```bash
# Import JSON file
mongoimport --db college_ems --collection students --file students.json --jsonArray
```

---

## Deployment Guide

### Production Environment Setup

#### 1. Server Requirements

**Minimum Specifications:**
- **OS:** Ubuntu 20.04 LTS / Windows Server 2019
- **CPU:** 2 cores
- **RAM:** 4 GB
- **Storage:** 20 GB SSD
- **Network:** Static IP, open ports 80, 443

**Recommended:**
- **CPU:** 4+ cores
- **RAM:** 8+ GB
- **Storage:** 50+ GB SSD
- **Backup:** Automated daily backups

#### 2. Install Dependencies

**Ubuntu/Linux:**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.8+
sudo apt install python3 python3-pip python3-venv -y

# Install MongoDB
wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/4.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list
sudo apt update
sudo apt install -y mongodb-org

# Start MongoDB
sudo systemctl start mongod
sudo systemctl enable mongod

# Install Nginx
sudo apt install nginx -y

# Install Certbot for SSL
sudo apt install certbot python3-certbot-nginx -y
```

**Windows Server:**
- Install Python 3.8+ from python.org
- Install MongoDB Community Edition
- Consider IIS or install Nginx for Windows

#### 3. Clone & Setup Application

```bash
# Create application directory
sudo mkdir -p /var/www/college-ems
cd /var/www/college-ems

# Clone repository
git clone <repository-url> .

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
cd backend
pip install -r requirements.txt
pip install gunicorn  # Production WSGI server
```

#### 4. Configure Environment

```bash
# Create production .env file
sudo nano backend/.env
```

**Production .env:**
```env
# Flask Configuration
SECRET_KEY=<generate-strong-random-key>
JWT_SECRET_KEY=<generate-different-strong-key>

# MongoDB Configuration
MONGO_URI=mongodb://localhost:27017/
DATABASE_NAME=college_ems_prod

# Admin Credentials
ADMIN_EMAIL=admin@yourdomain.com
ADMIN_PASSWORD=<strong-password>

# Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=notifications@yourdomain.com
MAIL_PASSWORD=<app-password>
MAIL_DEFAULT_SENDER=notifications@yourdomain.com

# Application Settings
FLASK_ENV=production
FLASK_DEBUG=False
```

**Generate Secure Keys:**
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

#### 5. Configure MongoDB for Production

```bash
# Enable MongoDB authentication
sudo nano /etc/mongod.conf
```

Add/modify:
```yaml
security:
  authorization: enabled

net:
  bindIp: 127.0.0.1
```

**Create MongoDB User:**
```bash
mongosh
```

```javascript
use admin
db.createUser({
  user: "emsadmin",
  pwd: "strong-password-here",
  roles: [{ role: "readWrite", db: "college_ems_prod" }]
})
```

Update MONGO_URI in .env:
```env
MONGO_URI=mongodb://emsadmin:strong-password-here@localhost:27017/college_ems_prod?authSource=admin
```

#### 6. Set Up Gunicorn

**Create Gunicorn service:**
```bash
sudo nano /etc/systemd/system/college-ems.service
```

**Service configuration:**
```ini
[Unit]
Description=College EMS Gunicorn Service
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/college-ems/backend
Environment="PATH=/var/www/college-ems/venv/bin"
ExecStart=/var/www/college-ems/venv/bin/gunicorn \
    --workers 4 \
    --bind unix:/var/www/college-ems/college-ems.sock \
    --access-logfile /var/log/college-ems/access.log \
    --error-logfile /var/log/college-ems/error.log \
    --log-level info \
    app:app

[Install]
WantedBy=multi-user.target
```

**Create log directory:**
```bash
sudo mkdir -p /var/log/college-ems
sudo chown www-data:www-data /var/log/college-ems
```

**Enable and start service:**
```bash
sudo systemctl start college-ems
sudo systemctl enable college-ems
sudo systemctl status college-ems
```

#### 7. Configure Nginx

**Create Nginx configuration:**
```bash
sudo nano /etc/nginx/sites-available/college-ems
```

**Nginx configuration:**
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    # Redirect HTTP to HTTPS (after SSL setup)
    # return 301 https://$server_name$request_uri;

    client_max_body_size 10M;

    # Frontend static files
    location / {
        root /var/www/college-ems/frontend;
        try_files $uri $uri/ /index.html;
    }

    # API proxy to Gunicorn
    location /api {
        proxy_pass http://unix:/var/www/college-ems/college-ems.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }

    # Health check endpoint
    location /api/health {
        proxy_pass http://unix:/var/www/college-ems/college-ems.sock;
        access_log off;
    }

    # Static files (CSS, JS, images)
    location ~* \.(css|js|png|jpg|jpeg|gif|ico|svg)$ {
        root /var/www/college-ems/frontend;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

**Enable site:**
```bash
sudo ln -s /etc/nginx/sites-available/college-ems /etc/nginx/sites-enabled/
sudo nginx -t  # Test configuration
sudo systemctl restart nginx
```

#### 8. Set Up SSL/TLS (HTTPS)

**Install SSL certificate with Certbot:**
```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

Certbot automatically:
- Obtains certificate from Let's Encrypt
- Configures Nginx for HTTPS
- Sets up automatic renewal

**Manual SSL (if using custom certificate):**
```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /path/to/certificate.crt;
    ssl_certificate_key /path/to/private.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # ... rest of configuration
}
```

**Test SSL:**
```bash
# Check certificate
openssl s_client -connect yourdomain.com:443

# Test with curl
curl -I https://yourdomain.com
```

#### 9. Set Up Firewall

**Ubuntu UFW:**
```bash
sudo ufw allow 22/tcp   # SSH
sudo ufw allow 80/tcp   # HTTP
sudo ufw allow 443/tcp  # HTTPS
sudo ufw enable
sudo ufw status
```

#### 10. Configure Backup

**Create backup script:**
```bash
sudo nano /usr/local/bin/backup-college-ems.sh
```

**Backup script:**
```bash
#!/bin/bash
BACKUP_DIR="/var/backups/college-ems"
DATE=$(date +%Y%m%d-%H%M%S)
MONGO_USER="emsadmin"
MONGO_PASS="your-mongodb-password"

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup MongoDB
mongodump --username $MONGO_USER --password $MONGO_PASS \
  --authenticationDatabase admin \
  --db college_ems_prod \
  --out $BACKUP_DIR/mongodb-$DATE

# Backup application files
tar -czf $BACKUP_DIR/app-$DATE.tar.gz /var/www/college-ems

# Remove backups older than 30 days
find $BACKUP_DIR -type f -mtime +30 -delete

echo "Backup completed: $DATE"
```

**Make executable:**
```bash
sudo chmod +x /usr/local/bin/backup-college-ems.sh
```

**Schedule daily backup (cron):**
```bash
sudo crontab -e
```

Add:
```cron
0 2 * * * /usr/local/bin/backup-college-ems.sh >> /var/log/college-ems/backup.log 2>&1
```

#### 11. Monitoring & Logging

**Install monitoring tools:**
```bash
# Install htop for system monitoring
sudo apt install htop -y

# Install logrotate for log management
sudo apt install logrotate -y
```

**Configure log rotation:**
```bash
sudo nano /etc/logrotate.d/college-ems
```

```
/var/log/college-ems/*.log {
    daily
    rotate 14
    compress
    delaycompress
    missingok
    notifempty
    create 0644 www-data www-data
    sharedscripts
    postrotate
        systemctl reload college-ems
    endscript
}
```

**Set up health check monitoring:**
```bash
# Create health check script
sudo nano /usr/local/bin/health-check.sh
```

```bash
#!/bin/bash
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost/api/health)

if [ $RESPONSE -ne 200 ]; then
    echo "Health check failed: HTTP $RESPONSE"
    # Send alert (email, SMS, etc.)
    echo "Alert: College EMS health check failed" | mail -s "EMS Alert" admin@yourdomain.com
    # Restart service
    systemctl restart college-ems
fi
```

**Schedule health check:**
```cron
*/5 * * * * /usr/local/bin/health-check.sh >> /var/log/college-ems/health-check.log 2>&1
```

#### 12. Performance Optimization

**Optimize MongoDB:**
```javascript
// Create indexes
use college_ems_prod
db.students.createIndex({ email: 1 }, { unique: true })
db.students.createIndex({ register_number: 1 }, { unique: true })
db.students.createIndex({ department: 1 })
db.events.createIndex({ date: 1 })
db.events.createIndex({ event_name: 1 })
db.attendance.createIndex({ student_id: 1, event_id: 1 }, { unique: true })
db.attendance.createIndex({ event_id: 1 })
db.attendance.createIndex({ attended_at: 1 })
```

**Configure Gunicorn workers:**
```
Workers = (2 x CPU cores) + 1
```

For 4-core server:
```bash
gunicorn --workers 9 ...
```

**Enable Nginx caching:**
```nginx
# Add to http block in /etc/nginx/nginx.conf
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=api_cache:10m max_size=100m inactive=60m;

# In server block
location /api {
    proxy_cache api_cache;
    proxy_cache_valid 200 5m;
    proxy_cache_bypass $http_cache_control;
    add_header X-Cache-Status $upstream_cache_status;
    # ... rest of proxy config
}
```

#### 13. Security Hardening

**Fail2ban for brute-force protection:**
```bash
sudo apt install fail2ban -y
sudo nano /etc/fail2ban/jail.local
```

```ini
[nginx-req-limit]
enabled = true
filter = nginx-req-limit
action = iptables-multiport[name=ReqLimit, port="http,https"]
logpath = /var/log/nginx/error.log
findtime = 600
bantime = 7200
maxretry = 10
```

**Restrict SSH access:**
```bash
sudo nano /etc/ssh/sshd_config
```

Change:
```
PermitRootLogin no
PasswordAuthentication no  # Use SSH keys only
```

**Enable automatic security updates:**
```bash
sudo apt install unattended-upgrades -y
sudo dpkg-reconfigure --priority=low unattended-upgrades
```

#### 14. Testing Deployment

**Test checklist:**
- [ ] Access https://yourdomain.com
- [ ] Student registration works
- [ ] Student login works
- [ ] Admin login works
- [ ] Event creation works
- [ ] QR code generation works
- [ ] QR code scanning works
- [ ] Attendance reports work
- [ ] Excel export works
- [ ] All API endpoints respond correctly
- [ ] SSL certificate valid
- [ ] Security headers present
- [ ] Rate limiting active

**Testing commands:**
```bash
# Test health endpoint
curl https://yourdomain.com/api/health

# Test SSL
curl -I https://yourdomain.com

# Check security headers
curl -I https://yourdomain.com

# Test rate limiting
for i in {1..60}; do curl https://yourdomain.com/api/health; done
```

---

### Docker Deployment (Alternative)

#### 1. Create Dockerfile

**backend/Dockerfile:**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]
```

#### 2. Create docker-compose.yml

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  mongodb:
    image: mongo:4.4
    container_name: college-ems-mongo
    restart: always
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: strongpassword
    volumes:
      - mongo-data:/data/db
    ports:
      - "27017:27017"

  backend:
    build: ./backend
    container_name: college-ems-backend
    restart: always
    environment:
      - MONGO_URI=mongodb://admin:strongpassword@mongodb:27017/college_ems?authSource=admin
      - FLASK_ENV=production
    depends_on:
      - mongodb
    ports:
      - "5000:5000"
    volumes:
      - ./backend:/app

  nginx:
    image: nginx:alpine
    container_name: college-ems-nginx
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./frontend:/usr/share/nginx/html
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - backend

volumes:
  mongo-data:
```

#### 3. Run with Docker

```bash
# Build and start containers
docker-compose up -d

# View logs
docker-compose logs -f

# Stop containers
docker-compose down

# Rebuild after changes
docker-compose up -d --build
```

---

### Cloud Deployment

#### AWS EC2

1. Launch EC2 instance (Ubuntu 20.04, t2.medium)
2. Configure security group (ports 22, 80, 443)
3. Follow Ubuntu deployment steps above
4. Use RDS for MongoDB (or DocumentDB)
5. Use S3 for backups
6. Use CloudWatch for monitoring

#### Google Cloud Platform

1. Create Compute Engine instance
2. Follow Ubuntu deployment steps
3. Use Cloud SQL or MongoDB Atlas
4. Use Cloud Storage for backups
5. Use Cloud Logging for logs

#### Microsoft Azure

1. Create Azure VM (Ubuntu)
2. Follow Ubuntu deployment steps
3. Use Azure Cosmos DB (MongoDB API)
4. Use Azure Blob Storage for backups
5. Use Azure Monitor for monitoring

#### Heroku (Quick Deploy)

```bash
# Create Procfile
echo "web: gunicorn --chdir backend app:app" > Procfile

# Create runtime.txt
echo "python-3.9.16" > runtime.txt

# Deploy
heroku create college-ems
heroku addons:create mongolab
git push heroku main
```

---

## Troubleshooting

### Common Issues & Solutions

#### 1. MongoDB Connection Failed

**Error:**
```
pymongo.errors.ServerSelectionTimeoutError: localhost:27017: [Errno 111] Connection refused
```

**Solutions:**
```bash
# Check if MongoDB is running
sudo systemctl status mongod

# Start MongoDB
sudo systemctl start mongod

# Check MongoDB logs
tail -f /var/log/mongodb/mongod.log

# Test connection
mongosh
```

**Windows:**
```powershell
# Start MongoDB service
net start MongoDB

# Or run manually
"C:\Program Files\MongoDB\Server\4.4\bin\mongod.exe" --dbpath="C:\data\db"
```

---

#### 2. Virtual Environment Issues

**Error:**
```
Module not found: flask
```

**Solutions:**
```bash
# Ensure venv is activated
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows

# Check Python version in venv
which python  # Should show venv path
python --version

# Reinstall dependencies
pip install -r requirements.txt

# If pip is outdated
python -m pip install --upgrade pip
```

---

#### 3. Port Already in Use

**Error:**
```
OSError: [Errno 98] Address already in use
```

**Solutions:**

**Linux/Mac:**
```bash
# Find process using port 5000
sudo lsof -i :5000

# Kill process
kill -9 <PID>

# Or use different port
python app.py --port 5001
```

**Windows:**
```powershell
# Find process
netstat -ano | findstr :5000

# Kill process
taskkill /PID <PID> /F
```

---

#### 4. CORS Errors in Browser

**Error:**
```
Access to fetch at 'http://localhost:5000/api/auth/login' from origin 'http://localhost:3000' 
has been blocked by CORS policy
```

**Solutions:**

**In backend/app.py:**
```python
# Ensure CORS is configured
from flask_cors import CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})

# For specific origin:
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})
```

**Check headers:**
```bash
curl -H "Origin: http://localhost:3000" -I http://localhost:5000/api/health
```

---

#### 5. JWT Token Expired

**Error:**
```json
{
  "success": false,
  "message": "Token has expired"
}
```

**Solutions:**

**Frontend:**
```javascript
// Clear expired token
localStorage.removeItem('token');
window.location.href = '/pages/login.html';
```

**Adjust expiration in config.py:**
```python
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=48)  # Extend to 48 hours
```

---

#### 6. QR Code Not Scanning

**Issues:**
- Camera not detected
- QR code blurry
- Poor lighting

**Solutions:**

**Browser Permissions:**
```javascript
// Check camera permission
navigator.mediaDevices.getUserMedia({ video: true })
  .then(stream => console.log('Camera access granted'))
  .catch(err => console.error('Camera access denied:', err));
```

**Test URLs:**
- Use `https://` (camera requires secure context)
- Or use `localhost` (exempt from secure context requirement)

**QR Code Quality:**
- Print in high resolution
- Ensure minimum 2x2 inches size
- Use good lighting when scanning
- Hold steady for 1-2 seconds

---

#### 7. Attendance Not Marking

**Error:**
```json
{
  "success": false,
  "message": "You are not registered for this event"
}
```

**Debug Steps:**

1. **Check if student registered:**
```javascript
// In MongoDB
db.students.findOne({ email: "student@example.com" })
// Check registered_events array
```

2. **Verify ObjectId types:**
```javascript
// Run check_data_types.py
python check_data_types.py
```

3. **Check QR data:**
```javascript
console.log('QR Data:', qrData);
// Should contain event_id and qr_token
```

4. **Verify backend logs:**
```bash
# Check for errors
tail -f /var/log/college-ems/error.log
```

---

#### 8. Excel Export Not Working

**Error:**
```
ModuleNotFoundError: No module named 'openpyxl'
```

**Solution:**
```bash
pip install openpyxl==3.1.2
```

**Browser Download Issues:**

**Check response headers:**
```python
# In backend/routes/attendance.py
response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
response.headers['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
```

---

#### 9. Email Notifications Not Sending

**Error:**
```
SMTPAuthenticationError: Username and Password not accepted
```

**Solutions:**

**Gmail:**
1. Enable 2-Step Verification
2. Generate App Password
3. Use app password in MAIL_PASSWORD

**Test email:**
```python
python
>>> from backend.utils.email_service import EmailService
>>> EmailService.send_event_registration_confirmation('test@example.com', 'John', 'Test Event')
```

**Note:** Email is optional, system works without it

---

#### 10. Admin Can't Login

**Error:**
```json
{
  "success": false,
  "message": "Invalid admin credentials"
}
```

**Solutions:**

**Check .env file:**
```bash
cat backend/.env
# Verify ADMIN_EMAIL and ADMIN_PASSWORD
```

**Default credentials:**
- Email: admin@college.edu
- Password: Admin@123

**Reset admin password:**
```bash
# Edit backend/.env
ADMIN_PASSWORD=NewPassword@123
```

**Password requirements:**
- Minimum 8 characters
- At least 1 uppercase letter
- At least 1 lowercase letter
- At least 1 number
- At least 1 special character

---

#### 11. Database Data Type Mismatch

**Error:**
```
Attendance report shows 0 registered students
```

**Solution:**

**Run migration script:**
```bash
cd backend
python ../migrate_event_ids.py
```

**Verify fix:**
```bash
python ../check_data_types.py
```

**Expected output:**
```
Types Match: True
Query with ObjectId: <number> students
```

---

#### 12. Rate Limiting Issues

**Error:**
```json
{
  "success": false,
  "message": "Rate limit exceeded. Please try again later."
}
```

**Solutions:**

**Check current limits:**
```python
# In backend/config.py
RATELIMIT_ENABLED = True
# Default: 200 per day, 50 per hour
```

**Adjust limits:**
```python
# In backend/app.py limiter configuration
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["500 per day", "100 per hour"]  # Increased limits
)
```

**Clear rate limits (development):**
```bash
# Restart Flask application
# Limits reset on restart when using memory storage
```

---

#### 13. Static Files Not Loading

**Error:**
```
404 Not Found: /css/style.css
```

**Solutions:**

**Check file paths:**
```html
<!-- Correct path in HTML -->
<link rel="stylesheet" href="../css/style.css">
<script src="../js/events.js"></script>
```

**Flask static configuration:**
```python
# In backend/app.py
app = Flask(__name__, 
            static_folder='../frontend', 
            static_url_path='')
```

**Nginx configuration:**
```nginx
location / {
    root /var/www/college-ems/frontend;
    try_files $uri $uri/ /index.html;
}
```

---

#### 14. Talisman HTTPS Issues (Development)

**Error:**
```
ERR_SSL_PROTOCOL_ERROR
```

**Solution:**

**Ensure development mode:**
```env
# In backend/.env
FLASK_ENV=development
```

**Verify Talisman is disabled:**
```python
# In backend/app.py
if os.getenv('FLASK_ENV') == 'production':
    Talisman(app, ...)
else:
    logging.info("Development mode - Talisman security headers disabled")
```

---

### Debug Mode

**Enable detailed error messages:**

```python
# In backend/app.py (development only)
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

**Check logs:**
```bash
# Application logs
tail -f /var/log/college-ems/error.log

# Nginx logs
tail -f /var/log/nginx/error.log

# MongoDB logs
tail -f /var/log/mongodb/mongod.log
```

---

### Getting Help

**Check documentation:**
1. README.md
2. SECURITY.md
3. CREDENTIALS.md
4. This document (PROJECT_DOCUMENTATION.md)

**Verify setup:**
1. Run check_data_types.py
2. Test API endpoints with curl/Postman
3. Check browser console for errors
4. Review server logs

**Common debugging tools:**
```bash
# Test API endpoint
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test@123"}'

# Check MongoDB data
mongosh college_ems
> db.students.find().pretty()
> db.events.find().pretty()

# Test connectivity
ping localhost
telnet localhost 5000
telnet localhost 27017
```

---

## Credentials & Access

### Default Admin Credentials

**Admin Login:**
- **URL:** http://localhost:5000/pages/admin_login.html
- **Email:** admin@college.edu
- **Password:** Admin@123

**⚠️ IMPORTANT:** Change the admin password before production deployment!

**Change Password:**
```bash
# Edit backend/.env file
ADMIN_PASSWORD=YourStrongPassword@2026
```

### Test Student Accounts

**Student 1:**
- Name: SANJAYKUMAR M
- Email: sanjay@college.edu
- Password: Sanjay@123
- Register Number: 927623BCS096
- Department: Computer Science
- Year: 3rd Year

**Student 2:**
- Name: BALU
- Email: balu@college.edu
- Password: Balu@123
- Register Number: 1026
- Department: Information Technology
- Year: 2nd Year

**Note:** These are sample accounts created during testing. You can create new accounts through registration.

### Database Access

**MongoDB Connection:**
```
mongodb://localhost:27017/
```

**Database Name:**
```
college_ems
```

**Collections:**
- students
- events
- attendance
- unauthorized_scans

**Access via MongoDB Shell:**
```bash
mongosh
use college_ems
db.students.find().pretty()
```

**Access via Python:**
```python
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client['college_ems']
print(db.students.count_documents({}))
```

### API Access

**Base URL:**
```
http://localhost:5000/api
```

**Get JWT Token:**
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"sanjay@college.edu","password":"Sanjay@123"}'
```

**Use Token:**
```bash
curl -H "Authorization: Bearer <token>" \
  http://localhost:5000/api/student/profile
```

### Environment Variables

Location: `backend/.env`

**Required Variables:**
```env
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
MONGO_URI=mongodb://localhost:27017/
DATABASE_NAME=college_ems
ADMIN_EMAIL=admin@college.edu
ADMIN_PASSWORD=Admin@123
FLASK_ENV=development
```

### Security Notes

1. **Never commit .env file to version control**
2. **Change all default passwords in production**
3. **Use strong random keys for SECRET_KEY and JWT_SECRET_KEY**
4. **Enable MongoDB authentication in production**
5. **Use HTTPS in production**
6. **Restrict CORS origins in production**

---

## Development

### Setting Up Development Environment

#### 1. Install Development Tools

**Code Editor:**
- Visual Studio Code (recommended)
- PyCharm
- Sublime Text

**VS Code Extensions:**
- Python
- Pylance
- MongoDB for VS Code
- REST Client (for API testing)

#### 2. Clone Repository

```bash
git clone <repository-url>
cd EMS
```

#### 3. Install Dependencies

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

#### 4. Configure Development Environment

```bash
# Copy example env file
cp .env.example .env

# Edit for development
nano .env
```

**Development .env:**
```env
FLASK_ENV=development
FLASK_DEBUG=True
MONGO_URI=mongodb://localhost:27017/
DATABASE_NAME=college_ems_dev
SECRET_KEY=dev-secret-key
JWT_SECRET_KEY=dev-jwt-secret
ADMIN_EMAIL=admin@college.edu
ADMIN_PASSWORD=Admin@123
```

#### 5. Run Development Server

```bash
# From backend directory with venv activated
python app.py
```

Server runs on http://localhost:5000 with auto-reload enabled.

### Code Structure Best Practices

#### Backend

**Models (backend/models/):**
```python
# Each model in separate file
# Example: student.py
class Student:
    @staticmethod
    def create(data):
        # Create student
        pass
    
    @staticmethod
    def find_by_email(email):
        # Find student
        pass
```

**Routes (backend/routes/):**
```python
# Each blueprint in separate file
# Example: student.py
from flask import Blueprint
student_bp = Blueprint('student', __name__)

@student_bp.route('/profile', methods=['GET'])
def get_profile():
    # Get student profile
    pass
```

**Utils (backend/utils/):**
```python
# Utility classes/functions
# Example: validators.py
class Validators:
    @staticmethod
    def validate_email(email):
        # Email validation logic
        pass
```

#### Frontend

**JavaScript:**
```javascript
// Each page has its own JS file
// Example: events.js

// API base URL
const API_BASE_URL = '/api';

// Get token
const token = localStorage.getItem('token');

// Make authenticated request
fetch(`${API_BASE_URL}/student/events`, {
    headers: {
        'Authorization': `Bearer ${token}`
    }
})
```

**HTML:**
```html
<!-- Use semantic HTML -->
<main>
    <section class="events-container">
        <h2>Available Events</h2>
        <div id="eventsGrid" class="events-grid">
            <!-- Events loaded dynamically -->
        </div>
    </section>
</main>
```

**CSS:**
```css
/* Use CSS variables */
:root {
    --primary-color: #667eea;
    --secondary-color: #764ba2;
    --success-color: #48bb78;
    --error-color: #f56565;
}

/* Mobile-first approach */
.container {
    width: 100%;
}

@media (min-width: 768px) {
    .container {
        width: 750px;
    }
}
```

### Testing

#### Manual Testing

**API Testing with curl:**
```bash
# Test registration
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "phone": "1234567890",
    "register_number": "TEST001",
    "department": "Computer Science",
    "course": "B.E. Computer Science",
    "year": "3rd Year",
    "password": "Test@123"
  }'

# Test login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test@123"}'
```

**Browser Testing:**
1. Open http://localhost:5000
2. Test student registration flow
3. Test student login
4. Test event registration
5. Test QR scanning (requires HTTPS or localhost)
6. Test admin dashboard
7. Test attendance reports

#### Unit Testing (Future Enhancement)

**Example test structure:**
```python
# tests/test_student.py
import unittest
from models.student import Student

class TestStudent(unittest.TestCase):
    def setUp(self):
        # Set up test data
        pass
    
    def test_create_student(self):
        # Test student creation
        pass
    
    def test_validate_email(self):
        # Test email validation
        pass
```

**Run tests:**
```bash
python -m unittest discover tests
```

### Git Workflow

#### Branching Strategy

```bash
# Main branches
main          # Production-ready code
development   # Development branch

# Feature branches
feature/qr-enhancement
feature/new-report
bugfix/attendance-issue

# Workflow
git checkout development
git checkout -b feature/new-feature
# Make changes
git add .
git commit -m "Add new feature"
git push origin feature/new-feature
# Create pull request to development
```

#### Commit Messages

**Format:**
```
<type>: <subject>

<body>

<footer>
```

**Types:**
- feat: New feature
- fix: Bug fix
- docs: Documentation
- style: Formatting
- refactor: Code restructuring
- test: Adding tests
- chore: Maintenance

**Examples:**
```bash
git commit -m "feat: Add Excel export for attendance reports"
git commit -m "fix: Resolve ObjectId type mismatch in attendance"
git commit -m "docs: Update API documentation with new endpoints"
```

### Code Review Checklist

- [ ] Code follows project structure
- [ ] All functions have docstrings
- [ ] Input validation implemented
- [ ] Error handling present
- [ ] Security considerations addressed
- [ ] No hardcoded credentials
- [ ] Comments for complex logic
- [ ] Consistent naming conventions
- [ ] No debug print statements
- [ ] Frontend uses escapeHtml for user input
- [ ] API endpoints documented
- [ ] Tests pass (if implemented)

### Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Commit with clear messages
6. Push to your fork
7. Create pull request

---

## Maintenance

### Regular Maintenance Tasks

#### Daily

- [ ] Monitor error logs
- [ ] Check system health
- [ ] Verify backup completion
- [ ] Review unauthorized scans

#### Weekly

- [ ] Review attendance reports
- [ ] Check disk space
- [ ] Update student information
- [ ] Archive old data (if needed)

#### Monthly

- [ ] Update dependencies
- [ ] Security audit
- [ ] Performance review
- [ ] Database optimization
- [ ] Backup verification

#### Yearly

- [ ] Full system audit
- [ ] SSL certificate renewal
- [ ] Major version upgrades
- [ ] Disaster recovery test

### Database Maintenance

**Optimize Database:**
```javascript
// MongoDB shell
use college_ems
db.repairDatabase()
db.students.reIndex()
db.events.reIndex()
db.attendance.reIndex()
```

**Clean Old Data:**
```javascript
// Remove old unauthorized scans (older than 6 months)
db.unauthorized_scans.deleteMany({
    scanned_at: { $lt: new Date(Date.now() - 6 * 30 * 24 * 60 * 60 * 1000) }
})

// Archive old events
db.events.updateMany(
    { date: { $lt: "2025-01-01" } },
    { $set: { archived: true } }
)
```

**Check Database Size:**
```javascript
db.stats()
db.students.stats()
db.events.stats()
db.attendance.stats()
```

### Updating Dependencies

**Check for updates:**
```bash
cd backend
pip list --outdated
```

**Update specific package:**
```bash
pip install --upgrade flask
```

**Update all (carefully):**
```bash
pip install --upgrade -r requirements.txt
```

**Test after updates:**
```bash
python app.py
# Run through testing checklist
```

### Log Management

**View recent logs:**
```bash
# Application logs
tail -n 100 /var/log/college-ems/error.log

# Access logs
tail -n 100 /var/log/nginx/access.log

# Follow live logs
tail -f /var/log/college-ems/error.log
```

**Analyze logs:**
```bash
# Count error occurrences
grep "Error" /var/log/college-ems/error.log | wc -l

# Find 404 errors
grep "404" /var/log/nginx/access.log

# Most accessed endpoints
awk '{print $7}' /var/log/nginx/access.log | sort | uniq -c | sort -rn | head
```

**Clear old logs:**
```bash
# Manually clear logs older than 30 days
find /var/log/college-ems -name "*.log" -mtime +30 -delete
```

### Performance Monitoring

**System Resources:**
```bash
# CPU and memory
htop

# Disk usage
df -h

# MongoDB stats
mongo
> db.serverStatus()
> db.currentOp()
```

**Application Metrics:**
```bash
# Request count
grep "GET\|POST" /var/log/nginx/access.log | wc -l

# Average response time
awk '{print $4}' /var/log/nginx/access.log | awk '{sum+=$1; n++} END {print sum/n}'
```

### Security Updates

**Update system packages:**
```bash
sudo apt update
sudo apt upgrade -y
```

**Check for vulnerabilities:**
```bash
# Python packages
pip-audit

# System vulnerabilities
sudo apt install lynis
sudo lynis audit system
```

**Review security logs:**
```bash
# Check authentication logs
sudo tail -f /var/log/auth.log

# Check firewall logs
sudo tail -f /var/log/ufw.log

# Check fail2ban
sudo fail2ban-client status
```

---

## Version History

### Version 1.0 (Current)

**Release Date:** March 3, 2026

**Features:**
- Student registration and authentication
- Event management system
- QR code generation and scanning
- Attendance tracking
- Excel report export
- Admin dashboard
- Security features (JWT, bcrypt, rate limiting)
- Input validation and sanitization
- Responsive design
- MongoDB integration

**Recent Fixes:**
- Fixed ObjectId type mismatch in registered_events
- Resolved CSP violations with relative API URLs
- Made Talisman production-only
- Added missing validators package
- Created frontend security utilities

**Documentation:**
- Complete API documentation
- Security implementation guide
- Deployment instructions
- Troubleshooting guide
- Project documentation (this file)

---

## License

[Specify your license here]

**Copyright © 2026 [Your Organization Name]**

---

## Contact & Support

**Developer:** [Your Name]  
**Email:** [your-email@domain.com]  
**Institution:** [Your College/University Name]

**Repository:** [GitHub URL]  
**Documentation:** This file (PROJECT_DOCUMENTATION.md)  
**Issue Tracking:** [GitHub Issues URL]

---

## Appendix

### A. Keyboard Shortcuts

**Admin Dashboard:**
- `Ctrl + E`: Focus event name field
- `Ctrl + G`: Generate QR code
- `Ctrl + R`: Refresh attendance report

**Events Page:**
- `Ctrl + S`: Start QR scanning
- `Ctrl + P`: View profile
- `Ctrl + L`: Logout

### B. File Locations

**Windows:**
```
Application: C:\Users\<user>\project\EMS\
Backend: C:\Users\<user>\project\EMS\backend\
Frontend: C:\Users\<user>\project\EMS\frontend\
Env File: C:\Users\<user>\project\EMS\backend\.env
```

**Linux:**
```
Application: /var/www/college-ems/
Backend: /var/www/college-ems/backend/
Frontend: /var/www/college-ems/frontend/
Env File: /var/www/college-ems/backend/.env
Logs: /var/log/college-ems/
```

### C. Port Numbers

- **5000**: Flask development server
- **8000**: Gunicorn production server
- **27017**: MongoDB
- **80**: HTTP (Nginx)
- **443**: HTTPS (Nginx)

### D. Useful Commands

**Start Application:**
```bash
.\start.bat                    # Windows quick start
python backend/app.py          # Manual start
gunicorn --chdir backend app:app  # Production
```

**Database Operations:**
```bash
mongosh                        # MongoDB shell
mongodump --db college_ems     # Backup
mongorestore                   # Restore
```

**Service Management:**
```bash
sudo systemctl start college-ems    # Start service
sudo systemctl stop college-ems     # Stop service
sudo systemctl restart college-ems  # Restart service
sudo systemctl status college-ems   # Check status
```

### E. Glossary

**Terms:**
- **JWT**: JSON Web Token (authentication token)
- **QR**: Quick Response (2D barcode)
- **CORS**: Cross-Origin Resource Sharing
- **CSP**: Content Security Policy
- **HSTS**: HTTP Strict Transport Security
- **ObjectId**: MongoDB unique identifier (12-byte)
- **bcrypt**: Password hashing algorithm
- **WSGI**: Web Server Gateway Interface

---

**End of Documentation**

---

**Document Information:**
- **File:** PROJECT_DOCUMENTATION.md
- **Lines:** 4000+
- **Last Updated:** March 3, 2026
- **Version:** 1.0
- **Format:** Markdown

---

*This documentation is comprehensive and should cover all aspects of the College Event Management System. For specific questions or issues not covered here, please refer to other documentation files or contact support.*
