# College Event Management System - Setup Guide

## Quick Start (5 Minutes)

### 1. Install MongoDB
Download and install: https://www.mongodb.com/try/download/community

**Windows:**
- Run the installer
- Choose "Complete" installation
- Install as a Windows Service
- MongoDB Compass (GUI) is optional

**Verify Installation:**
```bash
mongosh
```
If you see MongoDB shell, you're good to go!

### 2. Install Python Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 3. Create Environment File
```bash
# Copy example file
copy .env.example .env

# Edit .env with your settings (optional for development)
notepad .env
```

### 4. Run the Application
```bash
python app.py
```

### 5. Access the Application
Open browser: http://localhost:5000

---

## Testing the Application

### Test Student Flow:

1. **Register a Student**
   - Go to: http://localhost:5000/pages/register.html
   - Fill in details:
     - Name: John Doe
     - Register Number: CS2023001
     - Department: Computer Science
     - Year: 2
     - Email: john@example.com
     - Phone: 9876543210
     - Password: Pass123
   - Submit

2. **Login**
   - Go to: http://localhost:5000/pages/login.html
   - Email: john@example.com
   - Password: Pass123

3. **Register for Events**
   - Select events you want to participate
   - Submit registration

4. **View Success Page**
   - See confirmation message
   - Your registered events

### Test Admin Flow:

1. **Admin Login**
   - Go to: http://localhost:5000/pages/admin_login.html
   - Email: admin@college.edu
   - Password: Admin@123

2. **View Dashboard**
   - See statistics
   - Event registrations
   - Department breakdown

3. **Generate QR Code**
   - Select an event
   - Click "Generate QR Code"
   - Download the QR image

4. **Mark Attendance (Student side)**
   - Go to: http://localhost:5000/pages/scan.html
   - Login as student
   - Copy the QR code data (JSON format from generated QR)
   - Paste and mark attendance

5. **View Attendance Report**
   - Back to admin dashboard
   - Select event
   - Click "View Report"
   - Export to Excel

---

## Configuration Options

### Email Setup (Optional)

For Gmail:
1. Enable 2-factor authentication
2. Generate app password: https://myaccount.google.com/apppasswords
3. Update .env:
```env
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-16-character-app-password
```

### Change Admin Credentials

Edit `.env`:
```env
ADMIN_EMAIL=youradmin@college.edu
ADMIN_PASSWORD=YourSecurePassword123!
```

### MongoDB Custom Configuration

Edit `.env`:
```env
MONGO_URI=mongodb://username:password@localhost:27017/
DATABASE_NAME=my_custom_db_name
```

---

## Common Issues & Solutions

### Issue: "Module not found"
**Solution:**
```bash
pip install -r requirements.txt --upgrade
```

### Issue: "MongoDB connection failed"
**Solution:**
```bash
# Start MongoDB service
net start MongoDB

# Or check if running
mongosh
```

### Issue: "Port 5000 already in use"
**Solution:**
```bash
# Windows - Find and kill process
netstat -ano | findstr :5000
taskkill /PID <PID_NUMBER> /F

# Or change port in app.py:
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Issue: "Email not sending"
**Solution:**
- Emails are optional for testing
- App will work without email configuration
- Check console for email-related logs

### Issue: "CORS errors in browser"
**Solution:**
- Ensure backend is running
- Check API_BASE_URL in JavaScript files matches your backend URL
- Verify Flask-CORS is installed

---

## Project Structure Explained

```
EMS/
├── backend/
│   ├── app.py              ← Start here! Main Flask application
│   ├── config.py           ← Configure settings
│   ├── models/             ← Database models (MongoDB)
│   ├── routes/             ← API endpoints
│   └── utils/              ← Helper functions (QR, Email, etc.)
│
├── frontend/
│   ├── index.html          ← Landing page
│   ├── css/style.css       ← All styles
│   ├── js/                 ← JavaScript for each page
│   └── pages/              ← HTML pages
│
├── .env                    ← Configuration (create this!)
└── README.md               ← Documentation
```

---

## Database Overview

The system creates 4 MongoDB collections:

1. **students** - Student registrations
2. **events** - Event details (6 pre-configured)
3. **attendance** - Attendance records
4. **unauthorized_logs** - Security logs

**View Database:**
```bash
mongosh
use college_ems
db.students.find()
db.events.find()
db.attendance.find()
```

---

## API Testing with cURL

### Register Student:
```bash
curl -X POST http://localhost:5000/api/auth/register \
-H "Content-Type: application/json" \
-d "{\"name\":\"Test User\",\"register_number\":\"TEST001\",\"department\":\"CS\",\"year\":2,\"email\":\"test@test.com\",\"phone_number\":\"9876543210\",\"password\":\"Pass123\"}"
```

### Login:
```bash
curl -X POST http://localhost:5000/api/auth/login \
-H "Content-Type: application/json" \
-d "{\"email\":\"test@test.com\",\"password\":\"Pass123\"}"
```

### Get Events:
```bash
curl http://localhost:5000/api/student/events
```

---

## Development Tips

### Hot Reload (Auto-restart on changes):
```bash
# Install Flask in development mode
pip install flask[dotenv]

# Run with auto-reload
python app.py
# Changes to Python files will auto-restart the server
```

### Debug Mode:
Already enabled in `app.py`:
```python
app.run(debug=True, ...)
```

### View Logs:
The console will show:
- API requests
- Database queries
- Error messages
- Email sending status

---

## Production Deployment Checklist

- [ ] Change admin credentials in .env
- [ ] Generate strong SECRET_KEY and JWT_SECRET_KEY
- [ ] Configure MongoDB with authentication
- [ ] Set up SSL/TLS certificates
- [ ] Configure production email service
- [ ] Update CORS settings for your domain
- [ ] Set DEBUG=False in production
- [ ] Use a production WSGI server (Gunicorn, uWSGI)
- [ ] Set up database backups
- [ ] Configure firewall rules
- [ ] Set up monitoring and logging
- [ ] Review and adjust rate limits

---

## Minimum System Requirements

- **OS:** Windows 10/11, Linux, macOS
- **RAM:** 2GB minimum (4GB recommended)
- **Storage:** 1GB free space
- **Python:** 3.8 or higher
- **MongoDB:** 4.0 or higher
- **Browser:** Chrome, Firefox, Edge, Safari (latest versions)

---

## Getting Help

1. **Check logs** - Console output shows errors
2. **Verify MongoDB** - Ensure it's running
3. **Check dependencies** - Run `pip list`
4. **Test API** - Use browser or Postman
5. **Review code** - Error messages point to issues

---

## Next Steps

✅ Application is running successfully!

**For Students:**
- Register an account
- Explore events
- Test attendance marking

**For Admins:**
- Login to admin panel
- Generate QR codes
- View reports

**For Developers:**
- Explore the codebase
- Customize features
- Add new functionality

---

**🎉 Congratulations! Your College Event Management System is ready!**
