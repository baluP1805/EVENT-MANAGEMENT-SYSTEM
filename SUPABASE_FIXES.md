# Supabase Response Handling - All Fixes Applied

## Recent Fixes (March 5, 2026)

### Issue 1: Admin Dashboard Error - Missing RPC Function
**Error:** `Could not find the function public.count_students without parameters in the schema cache`

**Root Cause:** Code was calling `sb.rpc('count_students')` but the PostgreSQL function didn't exist in the database.

**Fix:** Updated `Student.count_students()` to use standard query with count instead of RPC:
```python
# BEFORE (BROKEN)
res = sb.rpc('count_students').execute()
return res.data if res else 0

# AFTER (FIXED)
res = sb.table('students').select('id', count='exact').execute()
return res.count if res and hasattr(res, 'count') else 0
```

### Issue 2: Invalid JSONB Data Error
**Error:** `invalid input syntax for type json - Token "69a6dcafc7b532b3ed54e87d" is invalid`

**Root Cause:** The `registered_events` JSONB column contained invalid data (likely from MongoDB ObjectId migration), and the `.contains()` query was trying to parse it as JSON.

**Fix:** 
1. Changed `Student.get_students_by_event()` to fetch all students and filter in Python instead of using JSONB contains operator:
```python
# BEFORE (BROKEN)
res = sb.table('students').select('*').contains('registered_events', [event_id]).execute()

# AFTER (FIXED)
res = sb.table('students').select('*').execute()
all_students = res.data or []
# Filter in Python to avoid JSONB parsing issues
filtered_students = [s for s in all_students 
                     if event_id in s.get('registered_events', [])]
```

2. Added JSONB validation and cleanup to migration script:
   - Converts NULL/invalid registered_events to empty array `[]`
   - Validates all registered_events are proper JSON arrays
   - Adds CHECK constraint to prevent future invalid data

3. Updated schema files with constraint:
```sql
CONSTRAINT registered_events_is_array CHECK (jsonb_typeof(registered_events) = 'array')
```

### Issue 3: Schema Field Mismatch
**Problem:** Events table schema didn't match application code expectations.

**Schema had:**
- `location`, `start_time`, `end_time`, `created_by`, `metadata`

**Code expected:**
- `venue`, `date`, `max_participants`, `total_registered`

**Fix:** Updated schema files:
- `backend/supabase_schema.sql` - For new installations (with default events)
- `backend/supabase_reset_schema.sql` - For complete reset (with default events)
- `backend/supabase_migration.sql` - For migrating existing databases

Migration script now:
- Migrates old field names to new ones (location → venue, start_time → date)
- Sets default values for missing fields
- Seeds 6 default events if table is empty
- Add proper indexes for performance

### Issue 4: Database Compatibility Fixes
**Issue:** Code using MongoDB-specific `_id` field instead of Supabase `id` field.

**Fix:** Updated all routes to use `InputSanitizer.get_id()` helper that works with both databases:
- Admin dashboard event ID extraction
- Department statistics 
- Attendance report student IDs
- Export attendance student IDs
- Unauthorized logs
- Attendance statistics

---

## Original Issue - Response Status Code

## Issue Identified
Error: `'APIResponse[TypeVar]' object has no attribute 'status_code'`

**Root Cause:** Supabase Python SDK v2.16+ doesn't expose `status_code` attribute on APIResponse objects. Instead:
- **Success:** Returns response object with `.data` attribute
- **Failure:** Raises an Exception (automatically)

## Fixes Applied

### 1. Student Model (`backend/models/student.py`)
**Fixed:** Student.create() method - removed status_code check
```python
# BEFORE
res = sb.table('students').insert(payload).execute()
if res.status_code in (200, 201):
    return res.data[0].get('id')
raise RuntimeError(...)

# AFTER
try:
    res = sb.table('students').insert(payload).execute()
    return res.data[0].get('id')
except Exception as e:
    raise RuntimeError('Failed to insert student into Supabase: ' + str(e))
```

### 2. Event Model (`backend/models/event.py`)
**Fixed:** 2 locations
- Event.create() - insert operation
- Event._seed_default_events() - bulk insert operation

Both now use try-except pattern instead of status_code checking.

### 3. Attendance Model (`backend/models/attendance.py`)
**Fixed:** Attendance.mark_attendance() - removed status_code check

### 4. UnauthorizedLog Model (`backend/models/unauthorized_log.py`)
**Fixed:** UnauthorizedLog.log_unauthorized_scan() - removed status_code check

## Response Handling Patterns Confirmed

### SELECT Operations (Already Correct)
```python
res = sb.table('students').select('*').eq('email', email).execute()
if res.data:
    return res.data[0]  # Correct pattern
```

### INSERT/UPDATE/DELETE Operations (Fixed)
```python
# Old pattern (BROKEN)
if res.status_code in (200, 201):  # ❌ No such attribute
    
# New pattern (CORRECT)
try:
    res = sb.table('table').insert(data).execute()  # Returns data on success
    return res.data[0].get('id')                      # ✅ Correct
except Exception as e:                                # ✅ Exceptions raised automatically
    raise RuntimeError('Error: ' + str(e))
```

## Files Modified

| File | Changes | Status |
|------|---------|--------|
| `backend/models/student.py` | create() method, count_students() | ✅ Fixed |
| `backend/models/event.py` | create() + _seed_default_events() | ✅ Fixed |
| `backend/models/attendance.py` | mark_attendance() | ✅ Fixed |
| `backend/models/unauthorized_log.py` | log_unauthorized_scan() | ✅ Fixed |
| `backend/routes/admin.py` | Cross-database ID handling | ✅ Fixed |
| `backend/supabase_schema.sql` | Events table fields, indexes | ✅ Fixed |
| `backend/supabase_reset_schema.sql` | Events table fields | ✅ Fixed |
| `backend/supabase_migration.sql` | Migration script | ✅ NEW |

## SQL Schema

All tables now have:
- Auto-generating UUIDs: `DEFAULT gen_random_uuid()::text`
- Proper CASCADE delete for foreign keys
- Performance indexes
- Correct field names matching application code

## Testing Checklist

- [x] All status_code references removed (5 total)
- [x] All INSERT/UPDATE/DELETE wrapped in try-except
- [x] SELECT operations verified (using res.data pattern)
- [x] Supabase UUID extension enabled in schema
- [x] Schema has ON DELETE CASCADE for referential integrity
- [x] RPC function replaced with standard query
- [x] Events table schema matches code expectations
- [x] Cross-database compatibility (MongoDB/_id vs Supabase/id)
- [x] Date handling for both datetime objects and ISO strings
- [x] Default events seeded in all schema files
- [x] Event fields (venue, date, max_participants, total_registered) properly configured

## Database Schema Summary

### Events Table
**Required Fields:**
- `id` (text, primary key, auto-generated UUID)
- `event_name` (text) - Name of the event
- `description` (text) - Event description
- `date` (text) - Event date (format: YYYY-MM-DD)
- `venue` (text) - Event location
- `max_participants` (integer) - Maximum number of participants
- `total_registered` (integer, default: 0) - Current registration count
- `created_at` (timestamptz) - Creation timestamp
- `updated_at` (timestamptz) - Last update timestamp

**Default Events Included:**
1. Paper Presentation - Mar 15, 2026 @ Main Auditorium (100 max)
2. Coding Contest - Mar 16, 2026 @ Computer Lab A (150 max)
3. Gaming Tournament - Mar 17, 2026 @ Gaming Arena (80 max)
4. Technical Quiz - Mar 18, 2026 @ Seminar Hall (120 max)
5. Project Expo - Mar 19, 2026 @ Exhibition Hall (200 max)
6. Debugging Challenge - Mar 20, 2026 @ Computer Lab B (100 max)

## How to Update Your Database

### Option 1: New Installation
```bash
# Copy backend/supabase_schema.sql to Supabase SQL Editor and execute
```

### Option 2: Complete Reset (WARNING: Deletes all data)
```bash
# Copy backend/supabase_reset_schema.sql to Supabase SQL Editor and execute
```

### Option 3: Migrate Existing Database (Recommended)
```bash
# Copy backend/supabase_migration.sql to Supabase SQL Editor and execute
# This will preserve your data while updating the schema
```

## How to Test Registration & Dashboard

```bash
# 1. Run schema update (choose one of the options above)

# 2. Test registration
# Navigate to registration page and create new student account

# 3. Test admin dashboard
# Login as admin and view dashboard
# Should show: total students, events, registrations without errors

# 4. Verify in Supabase
SELECT COUNT(*) FROM students;  -- Should include new registrations
SELECT * FROM events;  -- Should have venue, date, max_participants fields
```

## Key Takeaway

Supabase Python SDK automatically handles HTTP status codes internally. When using `.execute()`:
- **No exception = Success** (data available in `.data`)
- **Exception raised = Failure** (caught and handled in try-except)

No manual status code checking needed! ✅
