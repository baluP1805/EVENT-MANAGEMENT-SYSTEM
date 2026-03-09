# Testing Guide - QR Code Scanning System

## Quick Start Testing

### 1. Verify Backend is Running
```bash
# Navigate to project directory
cd /path/to/project

# Activate virtual environment (if using)
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Start Flask application
python backend/app.py
```

**Expected Output:**
```
 * Running on http://127.0.0.1:5000
 * Restarting with stat
 * Debugger is active!
```

---

### 2. Test QR Generator Utility (Standalone)

**Run Test Script:**
```bash
python test_qr_generator.py
```

**Expected Output:**
```
============================================================
QR Generator Verification Test
============================================================

✅ Test 1: Generate QR Code
Generated QR Data: {"event_id":"test-event-123","secure_token":"secure-token-abc","timestamp":"2024-03-05T10:30:00",...}
  • Event ID: test-event-123
  • Secure Token: secure-token-abc
  • Timestamp: 2024-03-05T10:30:00
  • Signature: abc123xyz789... (truncated)

✅ Test 2: Verify Valid QR Code
Verification Result: {'valid': True, 'event_id': 'test-event-123', ...}
  ✓ QR code is VALID
  • Event ID: test-event-123
  • Secure Token: secure-token-abc

✅ Test 3: Verify with Wrong Event ID (Should Fail)
Verification Result: {'valid': False, 'error': 'Event ID mismatch'}
  ✓ Correctly rejected: Event ID mismatch

✅ Test 4: Verify Tampered QR Code (Should Fail)
Verification Result: {'valid': False, 'error': 'Invalid signature'}
  ✓ Correctly rejected tampered data: Invalid signature

✅ Test 5: Verify Invalid JSON (Should Fail)
Verification Result: {'valid': False, 'error': 'Invalid JSON format'}
  ✓ Correctly rejected invalid JSON: Invalid JSON format

============================================================
All Tests Completed! ✅
============================================================
```

**If Any Test Fails:**
- Check `backend/config.py` → `JWT_SECRET_KEY` is set
- Verify `backend/utils/qr_generator.py` is present
- Check Python version (requires Python 3.7+)

---

### 3. Test API Endpoints with curl/Postman

#### A. Register Student
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Student",
    "register_number": "TEST2024001",
    "department": "Computer Science",
    "course": "B.Tech",
    "year": "3",
    "email": "test@example.com",
    "phone_number": "9876543210",
    "password": "Test123"
  }'
```

**Expected Response:**
```json
{
  "success": true,
  "message": "Registration successful! Please login.",
  "student_id": "uuid-here"
}
```

---

#### B. Login Student
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Test123"
  }'
```

**Expected Response:**
```json
{
  "success": true,
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "student": {
    "id": "uuid-here",
    "name": "Test Student",
    "email": "test@example.com"
  }
}
```

**Copy the JWT token** for subsequent requests!

---

#### C. Get Available Events
```bash
curl -X GET http://localhost:5000/api/student/events
```

**Expected Response:**
```json
{
  "success": true,
  "events": [
    {
      "id": "event-1",
      "event_name": "Technical Symposium 2024",
      "description": "Annual technical event",
      "date": "2024-03-15",
      "venue": "Main Auditorium",
      "max_participants": 200,
      "total_registered": 45
    },
    ...
  ]
}
```

**Copy an event ID** for registration!

---

#### D. Register for Event
```bash
curl -X POST http://localhost:5000/api/student/register-events \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE" \
  -d '{
    "event_ids": ["event-id-here"]
  }'
```

**Expected Response:**
```json
{
  "success": true,
  "message": "Successfully registered for 1 event",
  "registered_events": ["event-id-here"]
}
```

---

#### E. Generate QR Code (Admin)
```bash
curl -X GET http://localhost:5000/api/admin/generate-qr/event-id-here
```

**Expected Response:**
```json
{
  "success": true,
  "qr_data": "{\"event_id\":\"event-id-here\",\"secure_token\":\"abc123\",\"timestamp\":\"2024-03-05T10:30:00\",\"signature\":\"xyz789\"}",
  "event_name": "Technical Symposium 2024"
}
```

**Copy the qr_data** for scanning!

---

#### F. Scan QR Code (Mark Attendance)
```bash
curl -X POST http://localhost:5000/api/attendance/scan \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE" \
  -d '{
    "qr_data": "YOUR_QR_DATA_HERE"
  }'
```

**Expected Response (Success):**
```json
{
  "success": true,
  "message": "Attendance marked successfully for Technical Symposium 2024!",
  "attendance_id": "att-123",
  "student_name": "Test Student",
  "event_name": "Technical Symposium 2024"
}
```

**Expected Response (Not Registered):**
```json
{
  "success": false,
  "message": "You are not registered for Technical Symposium 2024. Unauthorized scan logged.",
  "unauthorized": true
}
```

**Expected Response (Already Marked):**
```json
{
  "success": false,
  "message": "Attendance already recorded for this event.",
  "marked_at": "2024-03-05T10:30:00"
}
```

---

### 4. Test Frontend UI

#### A. Student Registration Flow
1. Open: http://localhost:5000/pages/register.html
2. Fill form with test data
3. Click "Register"
4. **Verify:** Success message → Redirects to login page

#### B. Student Login Flow
1. Open: http://localhost:5000/pages/login.html
2. Enter registered email and password
3. Click "Login"
4. **Verify:** Redirects to events page

#### C. Event Registration Flow
1. After login, browse events
2. Select ONE event (checkbox)
3. Click "Register"
4. **Verify:** Success message displayed
5. **Check Database:** `students.registered_events` contains event ID

#### D. QR Code Scanning Flow (Camera)
1. Admin generates QR code for event
2. Student navigates to: http://localhost:5000/pages/scan.html
3. Click "Start Camera"
4. Grant camera permissions
5. Display QR code (print or on another device)
6. Scan QR code
7. **Verify:** 
   - Success message with event name
   - Attendance record created
   - Email sent (if configured)

#### E. QR Code Scanning Flow (Manual)
1. Copy QR data from admin panel
2. Navigate to: http://localhost:5000/pages/scan.html
3. Click "Manual Input" tab
4. Paste QR data
5. Click "Mark Attendance"
6. **Verify:** Same as camera scanning

---

### 5. Test Error Cases

#### A. Invalid JWT Token
```bash
curl -X POST http://localhost:5000/api/attendance/scan \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer invalid-token" \
  -d '{"qr_data": "..."}'
```

**Expected:**
```json
{
  "success": false,
  "message": "Invalid or expired token"
}
```

#### B. Expired QR Code
- Modify `QRGenerator.QR_EXPIRATION_SECONDS` to 1 second
- Generate QR code
- Wait 2 seconds
- Scan QR code

**Expected:**
```json
{
  "success": false,
  "message": "QR code has expired"
}
```

#### C. Tampered QR Signature
- Get valid QR data
- Modify any field (e.g., event_id)
- Attempt to scan

**Expected:**
```json
{
  "success": false,
  "message": "Invalid QR code signature"
}
```

#### D. Student Not Registered for Event
- Student registers for Event A
- Scans QR code for Event B

**Expected:**
```json
{
  "success": false,
  "message": "You are not registered for Event B. Unauthorized scan logged."
}
```

#### E. Duplicate Attendance
- Student marks attendance for Event A
- Attempts to scan same QR code again

**Expected:**
```json
{
  "success": false,
  "message": "Attendance already recorded for this event.",
  "marked_at": "2024-03-05T10:30:00"
}
```

---

### 6. Database Verification

#### Check Attendance Records
```sql
SELECT 
  a.id,
  s.name AS student_name,
  s.register_number,
  e.event_name,
  a.marked_at
FROM attendance a
JOIN students s ON a.student_id = s.id
JOIN events e ON a.event_id = e.id
ORDER BY a.marked_at DESC;
```

#### Check Unauthorized Scans
```sql
SELECT 
  qr_token,
  scan_data,
  scanned_at,
  ip_address
FROM unauthorized_logs
ORDER BY scanned_at DESC;
```

#### Check Event Registration Counts
```sql
SELECT 
  event_name,
  total_registered,
  max_participants,
  (max_participants - total_registered) AS slots_remaining
FROM events
ORDER BY total_registered DESC;
```

#### Verify JSONB Data Integrity
```sql
SELECT 
  name,
  register_number,
  registered_events,
  jsonb_typeof(registered_events) AS data_type
FROM students
WHERE jsonb_typeof(registered_events) != 'array';
```

**Expected:** Zero rows (all should be arrays)

---

### 7. Performance Testing

#### Load Test - Multiple Scans
```bash
# Install Apache Bench (if not available)
# Windows: Download from Apache website
# Linux: sudo apt install apache2-utils

# Test 100 concurrent requests
ab -n 100 -c 10 -H "Authorization: Bearer YOUR_TOKEN" \
   -T "application/json" \
   -p qr_data.json \
   http://localhost:5000/api/attendance/scan
```

**Expected:** 
- Average response time < 200ms
- Zero failed requests
- No database deadlocks

---

### 8. Security Testing

#### A. SQL Injection Test
```bash
# Try injecting SQL in event_id
curl -X POST http://localhost:5000/api/attendance/scan \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"qr_data": "{\"event_id\":\"1; DROP TABLE students;\",\"secure_token\":\"abc\",\"timestamp\":\"2024-01-01\",\"signature\":\"xyz\"}"}'
```

**Expected:** Sanitizer blocks the request, no database changes

#### B. XSS Test
```bash
# Try injecting script in name
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"<script>alert(\"XSS\")</script>","register_number":"XSS001",...}'
```

**Expected:** HTML entities escaped, no script execution

#### C. JWT Manipulation
- Copy valid JWT token
- Decode and modify payload (change student_id)
- Attempt to scan QR code

**Expected:** Token signature verification fails, request rejected

---

### 9. Email Testing

#### Verify Email Configuration
```bash
# Check .env file
cat .env | grep MAIL_
```

**Expected:**
```
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com
```

#### Test Email Service
```python
# Run in Python shell
python
>>> from backend.utils.email_service import EmailService
>>> EmailService.send_attendance_confirmation(
...     'test@example.com', 
...     'Test Student', 
...     'Technical Symposium 2024'
... )
True
```

**Expected:** Email received in inbox (check spam folder)

---

### 10. Monitoring & Logs

#### Watch Backend Logs
```bash
# Terminal 1: Start backend with logging
python backend/app.py

# Terminal 2: Watch for errors
tail -f backend/logs/app.log  # If logging to file
```

**Watch For:**
- ✅ `Email sent successfully to student@example.com`
- ✅ `Attendance marked: student_id=123, event_id=456`
- ⚠️ `Email service not configured. Skipping email notification.`
- ❌ `Invalid QR code signature detected`

#### Browser Console Logs
1. Open Browser DevTools (F12)
2. Navigate to Console tab
3. **Watch For:**
   - ✅ `Token stored successfully`
   - ✅ `Attendance marked successfully`
   - ❌ `API Error: 401 Unauthorized`

---

## Common Issues & Fixes

### Issue 1: "Token not found"
**Cause:** Student not logged in or JWT expired  
**Fix:** Re-login at `/pages/login.html`

### Issue 2: "Event not found"
**Cause:** Event ID doesn't exist in database  
**Fix:** Check event ID in QR data, verify with database

### Issue 3: "Invalid signature"
**Cause:** QR data tampered or JWT_SECRET_KEY changed  
**Fix:** Regenerate QR code with current secret key

### Issue 4: "Camera permission denied"
**Cause:** Browser blocked camera access  
**Fix:** Grant permissions in browser settings

### Issue 5: "Email not sending"
**Cause:** Email not configured (optional)  
**Fix:** See `EMAIL_SETUP.md` for configuration guide

### Issue 6: "JSONB error"
**Cause:** Legacy MongoDB ObjectId data in registered_events  
**Fix:** Run `backend/supabase_migration.sql` to clean data

---

## Success Criteria

### ✅ Core Functionality
- [ ] Students can register accounts
- [ ] Students can login and receive JWT
- [ ] Students can register for events
- [ ] Admin can generate QR codes
- [ ] Students can scan QR codes (camera or manual)
- [ ] Attendance is recorded correctly
- [ ] Duplicate attendance is prevented
- [ ] Unauthorized scans are logged

### ✅ Security
- [ ] JWT authentication works
- [ ] QR signature verification works
- [ ] Tampered QR codes are rejected
- [ ] Expired QR codes are rejected
- [ ] Input sanitization prevents XSS
- [ ] SQL injection attempts blocked

### ✅ Database Integrity
- [ ] No duplicate attendance records
- [ ] JSONB arrays are valid
- [ ] Foreign key constraints enforced
- [ ] Event registration counts accurate

### ✅ User Experience
- [ ] Clear error messages
- [ ] Success confirmations displayed
- [ ] Email notifications sent (if configured)
- [ ] UI responsive and functional

---

## Next Steps After Testing

1. **All Tests Pass:** Deploy to production (see `VERCEL_DEPLOYMENT.md`)
2. **Some Tests Fail:** Review logs, fix issues, re-test
3. **Email Issues:** Optional feature, can skip if not needed
4. **Performance Issues:** Add caching, optimize database queries

---

**Happy Testing! 🚀**

For detailed API documentation, see `PROJECT_DOCUMENTATION.md`  
For security best practices, see `SECURITY.md`  
For deployment guide, see `VERCEL_DEPLOYMENT.md`
