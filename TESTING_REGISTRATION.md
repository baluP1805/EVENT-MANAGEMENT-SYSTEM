# Quick Start Guide - Testing Updated Registration

## Start the Application

```powershell
cd c:\Users\sanja\project\EMS
.\start.bat
```

## Test the Registration System

### 1. Open Registration Page
```
http://localhost:5000/frontend/pages/register.html
```

### 2. Test Department & Course Selection

#### Test Management Department:
1. Select **Department**: `Management`
2. **Course dropdown** should show:
   - B.B.A
   - B.Com
   - B.Com CA (Computer Applications)
   - B.Com PA (Professional Accounting)
   - M.Com CA (Computer Applications)
   - MBA (AICTE Approved)
   - Ph.D. Commerce

#### Test Science Department:
1. Select **Department**: `Science`
2. **Course dropdown** should show:
   - B.Sc. Computer Science
   - B.C.A
   - B.Sc. Artificial Intelligence & Machine Learning
   - B.Sc. Mathematics
   - B.Sc. Physics
   - B.Sc. Fashion Technology & Costume Designing
   - B.Sc. Hotel Management & Catering Science
   - M.Sc. Computer Science
   - M.Sc. Mathematics

#### Test Arts Department:
1. Select **Department**: `Arts`
2. **Course dropdown** should show:
   - B.A. Tamil
   - B.A. English
   - B.A. Public Administration
   - M.A. English

### 3. Complete Registration

**Sample Test Data:**
```
Full Name: Test Student
Register Number: 21SCI001
Department: Science
Course: B.Sc. Computer Science
Year: 1st Year
Email: teststudent@example.com
Phone Number: 9876543210
Password: Test@123
```

**Click "Register"** → Should show success message and redirect to login

### 4. Login and Check Profile

1. Login with the registered email and password
2. Go to Events page
3. Click **Profile** button
4. Verify the profile shows:
   - ✅ Name
   - ✅ Register Number
   - ✅ Department: `Science`
   - ✅ **Course/Programme: `B.Sc. Computer Science`** ← NEW!
   - ✅ Year: `1st Year`
   - ✅ Email
   - ✅ Phone Number
   - ✅ Registered Events Count

---

## Validation Tests

### Test 1: Missing Course
1. Select department
2. **Don't select course**
3. Try to submit
4. Should show: "Course/Programme is required"

### Test 2: Invalid Department
Try submitting with invalid department (via browser console):
```javascript
fetch('http://localhost:5000/api/auth/register', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    name: 'Test',
    register_number: '123',
    department: 'Invalid Department',
    course: 'Test Course',
    year: '1st Year',
    email: 'test@test.com',
    phone_number: '9876543210',
    password: 'Test123'
  })
}).then(r => r.json()).then(console.log)
```
Should return: "Department must be one of: Management, Science, Arts"

### Test 3: Invalid Year
Try submitting with old year format:
```javascript
// Same as above but year: '1' instead of '1st Year'
```
Should return: "Year must be one of: 1st Year, 2nd Year, 3rd Year, 4th Year"

---

## Visual Verification

### Registration Form Layout:
```
┌─────────────────────────────────────────────────┐
│  Full Name              Register Number         │
├─────────────────────────────────────────────────┤
│  Department             Course/Programme        │
│  [Management ▼]         [Select Course... ▼]    │
├─────────────────────────────────────────────────┤
│  Year                   Phone Number            │
│  [1st Year ▼]           [9876543210]           │
├─────────────────────────────────────────────────┤
│  Email                                          │
│  [student@example.com]                          │
├─────────────────────────────────────────────────┤
│  Password                                       │
│  [••••••••]                                     │
├─────────────────────────────────────────────────┤
│           [Register Button]                     │
└─────────────────────────────────────────────────┘
```

### Profile Modal Display:
```
┌──────────────────────────────┐
│         Your Profile     [×] │
├──────────────────────────────┤
│ Name                         │
│ Student Name                 │
├──────────────────────────────┤
│ Register Number              │
│ 21SCI001                     │
├──────────────────────────────┤
│ Department                   │
│ Science                      │
├──────────────────────────────┤
│ Course/Programme         ← NEW│
│ B.Sc. Computer Science       │
├──────────────────────────────┤
│ Year                         │
│ 1st Year                     │
├──────────────────────────────┤
│ Email                        │
│ student@example.com          │
├──────────────────────────────┤
│ Phone Number                 │
│ 9876543210                   │
├──────────────────────────────┤
│ Registered Events            │
│ 0                            │
└──────────────────────────────┘
```

---

## Database Verification

### Check Registered Student:
```powershell
mongosh
use ems_db
db.students.findOne({email: "teststudent@example.com"})
```

Should show:
```javascript
{
  _id: ObjectId("..."),
  name: "Test Student",
  register_number: "21SCI001",
  department: "Science",
  course: "B.Sc. Computer Science",  // ← NEW FIELD
  year: "1st Year",                  // ← NEW FORMAT
  email: "teststudent@example.com",
  phone_number: "9876543210",
  password: "$2b$12$...",
  registered_events: [],
  created_at: ISODate("..."),
  updated_at: ISODate("...")
}
```

---

## Expected Behavior Summary

✅ **Department dropdown** - Shows 3 options (Management, Science, Arts)  
✅ **Course dropdown** - Disabled until department selected  
✅ **Course dropdown** - Populates based on selected department  
✅ **Course dropdown** - Changes when department changes  
✅ **Year dropdown** - Shows "1st Year", "2nd Year", "3rd Year", "4th Year"  
✅ **Form validation** - Requires all fields including course  
✅ **Backend validation** - Validates department, course, and year format  
✅ **Database storage** - Stores course in student document  
✅ **Profile display** - Shows course in profile modal  
✅ **Admin search** - Returns course field in student data  

---

## Troubleshooting

### Course dropdown not populating?
- Check browser console (F12) for JavaScript errors
- Verify department value is exactly "Management", "Science", or "Arts"
- Hard refresh page (Ctrl+F5)

### Registration fails with validation error?
- Check backend terminal for exact error message
- Verify all fields are filled
- Check year format is "1st Year" not "1"

### Profile doesn't show course?
- Check if student document in database has course field
- Students registered before update won't have course field
- Profile shows "N/A" if course field is missing

### Old students showing errors?
- Old students may have old department/year formats
- Profile will show "N/A" for missing course
- Consider running migration script to update old records

---

## Success Criteria

The update is working correctly when:

1. ✅ Registration form shows 3 departments
2. ✅ Course dropdown populates dynamically
3. ✅ All courses from image are available
4. ✅ Form submits successfully with course
5. ✅ Database stores course field
6. ✅ Profile modal displays course
7. ✅ No console errors
8. ✅ No backend errors

**If all tests pass, the registration system is ready to use!** 🎉
