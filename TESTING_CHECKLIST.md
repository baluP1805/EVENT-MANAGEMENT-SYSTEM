# 🧪 Testing Checklist - Events & Admin System

## ⚡ Quick Start
```powershell
# Start the system:
cd c:\Users\sanja\project\EMS
.\start.bat

# Open browser:
http://localhost:5000
```

---

## 📋 Testing Sequence

### ✅ Test 1: Events Page Display
**Goal:** Verify events load and display correctly after JavaScript fix

**Steps:**
1. Login as student:
   - Email: `sanjaykumarmsk509@gmail.com`
   - Password: (your password)
2. Navigate to Events page
3. **Hard refresh:** Press `Ctrl + F5` (clears cached JavaScript)
4. Wait 2-3 seconds for events to load

**Expected Results:**
- ✅ See 6 event cards displayed
- ✅ Each card has radio button (circle)
- ✅ Event details visible: name, date, venue, max participants
- ✅ No console errors (press F12 → Console tab)

**If events don't show:**
```javascript
// Open browser console (F12) and run:
localStorage.getItem('token')  // Should show a JWT token
fetch('http://localhost:5000/api/student/events', {
  headers: { 'Authorization': 'Bearer ' + localStorage.getItem('token') }
}).then(r => r.json()).then(console.log)  // Should show 6 events
```

---

### ✅ Test 2: Single Event Selection
**Goal:** Confirm only one event can be selected (radio button behavior)

**Steps:**
1. Click on "Paper Presentation" card
2. Click on "Coding Contest" card
3. Try clicking multiple events

**Expected Results:**
- ✅ Only one event can be selected at a time
- ✅ Previously selected event deselects automatically
- ✅ Selected card shows highlight/border
- ✅ Radio button shows checkmark

---

### ✅ Test 3: Event Registration
**Goal:** Verify registration stores data in database

**Steps:**
1. Select "Technical Quiz" (currently has 0 registrations)
2. Click "Submit Registration" button
3. Should redirect to success page or show confirmation

**Verify in Database:**
```powershell
# Run database check:
py check_db.py
```

**Expected Database Changes:**
- ✅ Student's `registered_events` array includes Technical Quiz ID
- ✅ Technical Quiz `total_registered` incremented from 0 to 1

---

### ✅ Test 4: Already Registered Student
**Goal:** Verify registered students see different view

**Steps:**
1. Logout
2. Login as student who already registered (SANJAYKUMAR M)
3. Navigate to Events page

**Expected Results:**
- ✅ See "Already Registered" badge at top
- ✅ Shows registered event card with details
- ✅ NO registration form visible
- ✅ Cannot register for more events

---

### ✅ Test 5: Profile Modal
**Goal:** Verify profile button and modal work

**Steps:**
1. Click "Profile" button (top right, near logout)
2. Modal should open

**Expected Results:**
- ✅ Modal opens with backdrop
- ✅ Shows 7 fields:
  - Full Name
  - Register Number
  - Email
  - Department
  - Academic Year
  - Phone Number
  - Registered Events Count
- ✅ Can close modal with X button or clicking backdrop

---

### ✅ Test 6: QR Scanner
**Goal:** Verify camera QR scanner works

**Steps:**
1. Click "Scan QR" button
2. Browser will ask for camera permission → Click "Allow"
3. Hold a QR code in front of camera

**Expected Results:**
- ✅ Camera feed appears in modal
- ✅ Scanner frame with corner decorations visible
- ✅ When QR detected, shows "Processing..." message
- ✅ Successful scan closes modal and shows success/error message

**Notes:**
- Use Chrome or Edge (best camera support)
- Requires HTTPS or localhost
- Test with any QR code first to verify camera works

---

### ✅ Test 7: Admin Dashboard - Overview
**Goal:** Verify admin can see all registration statistics

**Steps:**
1. Logout from student account
2. Login as admin:
   - Email: `admin@college.edu`
   - Password: `Admin@123`
3. Go to Admin Dashboard

**Expected Results:**
- ✅ Shows Total Students: `2`
- ✅ Shows Total Events: `6`
- ✅ Shows Event Registrations table with:
  - Event names
  - Total Registered counts
  - Total Attended counts
  - Attendance percentage
- ✅ Shows Department Statistics
- ✅ Shows Unauthorized Scans count

**Verify Data Matches:**
```
Paper Presentation - 1 registered
Coding Contest - 1 registered
Gaming Tournament - 1 registered
Technical Quiz - 0 or 1 (if you registered in Test 3)
Project Expo - 3 registered
Debugging Challenge - 0 registered
```

---

### ✅ Test 8: Admin - Student Search
**Goal:** Verify admin can search and view student registration data

**Steps:**
1. In admin dashboard, find "Student Search" section
2. Enter register number (e.g., student's register number)
3. Click "Search"

**Expected Results:**
- ✅ Shows student details:
  - Name
  - Register Number
  - Department
  - Year
  - Email
  - Phone Number
- ✅ Shows **Registered Events** list with event names
- ✅ If student registered for Coding Contest and Project Expo, shows both

**API Test:**
```javascript
// In browser console (F12):
fetch('http://localhost:5000/api/student/search/REGISTER_NUMBER_HERE', {
  headers: { 'Authorization': 'Bearer ' + localStorage.getItem('adminToken') }
}).then(r => r.json()).then(console.log)
```

---

### ✅ Test 9: Admin - Event Attendance Report
**Goal:** Verify admin can view detailed event reports

**Steps:**
1. In admin dashboard, find event list
2. Click "View Report" or similar for "Project Expo"
3. View attendance report

**Expected Results:**
- ✅ Shows event name: "Project Expo"
- ✅ Shows Total Registered: `3`
- ✅ Shows Total Attended: (number of students who scanned QR)
- ✅ Shows Total Absent: (registered - attended)
- ✅ Shows Attendance Percentage
- ✅ Shows list of attended students with:
  - Student Name
  - Register Number
  - Department
  - Year
  - Marked At (timestamp)

---

### ✅ Test 10: Admin - Generate QR Code
**Goal:** Verify admin can generate event QR codes

**Steps:**
1. Select an event (e.g., "Technical Quiz")
2. Click "Generate QR Code" button
3. QR code image appears

**Expected Results:**
- ✅ QR code image displays
- ✅ Can download QR code
- ✅ QR code contains event ID and secure token

**Test QR Code:**
1. Download/save the generated QR code
2. Login as student
3. Open QR scanner
4. Scan the downloaded QR code
5. Should mark attendance for that event

---

### ✅ Test 11: Data Consistency Check
**Goal:** Verify database counts match displayed counts

**Steps:**
1. Run database check script:
```powershell
py check_db.py
```

2. Compare with admin dashboard numbers

**Expected Results:**
- ✅ Event `total_registered` matches count in dashboard
- ✅ Student `registered_events` arrays match search results
- ✅ No orphaned references (event IDs that don't exist)

**Manual Verification:**
```javascript
// Check consistency:
db.events.find().forEach(event => {
  let actual_count = db.students.countDocuments({
    registered_events: event._id
  });
  let stored_count = event.total_registered;
  if (actual_count !== stored_count) {
    print(`❌ Mismatch for ${event.event_name}: actual=${actual_count}, stored=${stored_count}`);
  } else {
    print(`✅ ${event.event_name}: ${actual_count} registrations verified`);
  }
});
```

---

### ✅ Test 12: Export Functionality
**Goal:** Verify Excel export works

**Steps:**
1. In admin event report, click "Export to Excel"
2. Download Excel file

**Expected Results:**
- ✅ Excel file downloads successfully
- ✅ Contains all attendance data
- ✅ Proper formatting with headers
- ✅ Student details match database

---

## 🔍 Debugging Tools

### Check Browser Console
```javascript
// Press F12 → Console tab

// Check if token exists:
localStorage.getItem('token')

// Check student data:
localStorage.getItem('studentData')

// Test API directly:
fetch('http://localhost:5000/api/student/events', {
  headers: { 'Authorization': 'Bearer ' + localStorage.getItem('token') }
}).then(r => r.json()).then(console.log)

// Check for JavaScript errors:
// Look for red error messages in console
```

### Check MongoDB
```powershell
# Connect to MongoDB:
mongosh

# Switch to database:
use ems_db

# Count documents:
db.events.countDocuments()      # Should be 6
db.students.countDocuments()    # Should be 2+

# View all events:
db.events.find().pretty()

# View students with registrations:
db.students.find({}, {name:1, registered_events:1}).pretty()

# Check event registration count:
db.events.find({}, {event_name:1, total_registered:1}).pretty()
```

### Check Backend Logs
```powershell
# Backend should show:
# - API requests: GET /api/student/events
# - Registration: POST /api/student/register-events
# - Errors (if any) in red
```

---

## ⚠️ Common Issues & Fixes

### Issue 1: Events Not Displaying
**Symptoms:** Blank page after login

**Fixes:**
1. Hard refresh: `Ctrl + F5`
2. Clear browser cache
3. Check console for errors (F12)
4. Verify token: `localStorage.getItem('token')`
5. Test API manually (see debugging tools above)

---

### Issue 2: "Already Registered" Even Though Not Registered
**Cause:** SANJAYKUMAR M has 2 events from old multi-event system

**Fix:**
```javascript
// Clear old registrations:
db.students.updateOne(
  {email: 'sanjaykumarmsk509@gmail.com'},
  {$set: {registered_events: []}}
)
```

---

### Issue 3: Count Mismatch
**Symptoms:** Dashboard shows different number than database

**Fix:**
```javascript
// Recalculate all event counts:
db.events.find().forEach(event => {
  let count = db.students.countDocuments({
    registered_events: event._id
  });
  db.events.updateOne(
    {_id: event._id},
    {$set: {total_registered: count}}
  );
  print(`Updated ${event.event_name}: ${count}`);
});
```

---

### Issue 4: QR Scanner Not Working
**Causes:** 
- Wrong browser (use Chrome/Edge)
- Camera permission denied
- Not using HTTPS (localhost is ok)

**Fixes:**
1. Use Chrome or Edge browser
2. Grant camera permission when prompted
3. Check browser settings → Site settings → Camera
4. Test with different QR code

---

### Issue 5: Registration Fails
**Symptoms:** Error message after clicking submit

**Check:**
1. Is student already registered? (should show badge)
2. Is event at max capacity?
3. Check backend logs for error details
4. Verify token is valid: `jwt.decode(token)` in Python

---

## ✅ Success Criteria

**System is working correctly when:**

1. ✅ Events page displays all 6 events
2. ✅ Single event selection works (radio buttons)
3. ✅ Registration updates database (verified with `py check_db.py`)
4. ✅ Registered students see badge and registered event
5. ✅ Profile modal shows all student data
6. ✅ QR scanner opens camera and scans codes
7. ✅ Admin dashboard shows accurate statistics
8. ✅ Admin can search students and see their registrations
9. ✅ Admin event reports show all registered students
10. ✅ Database counts match displayed counts
11. ✅ Excel export works
12. ✅ No console errors (F12 → Console)

---

## 📊 Expected Test Results Summary

After completing all tests, you should have:

**Database State:**
- **Students:** 2+ (depending on new registrations)
- **Events:** 6 (unchanged)
- **Registrations:** Multiple students registered for various events
- **Attendance:** Records for QR scans

**Admin Dashboard Shows:**
- Total students count
- Total events: 6
- Registration statistics per event
- Department breakdown
- Ability to search any student
- Ability to view event reports
- Ability to export data

**Student Experience:**
- Can view all events
- Can register for one event only
- Can view profile
- Can scan QR codes
- Cannot register for multiple events
- If already registered, shows registered event instead of form

---

## 🎯 Next Steps After Testing

If all tests pass:
1. ✅ System is production-ready
2. Add more events if needed
3. Monitor registration counts
4. Generate QR codes for all events
5. Print QR codes for event venues

If tests fail:
1. Note which specific test failed
2. Check corresponding section in this guide
3. Run debugging commands provided
4. Check backend logs
5. Verify database state with `py check_db.py`

---

**Last Updated:** After JavaScript fix and database verification
**System Status:** ✅ All core features working
