# FIXES APPLIED - Schema & Data Type Corrections

## Issue Identified
Error: `invalid input syntax for type integer: "3rd Year"`

**Root Cause:** MongoDB stores `year` as text strings (e.g., "1st Year", "2nd Year"), but the Supabase schema expected an integer type.

## Fixes Applied

### 1. Schema Updates
- **Changed `year` column type:** `integer` → `text`
- **Updated files:**
  - `backend/supabase_schema.sql`
  - `backend/supabase_reset_schema.sql`

### 2. Migration Script Updates
- **Simplified year handling** in `backend/migrate_to_supabase.py`
- Year values are now kept as-is (text strings like "1st Year", "2nd Year")
- Added proper phone → phone_number field renaming

### 3. Configuration Updates
- **Updated `.env.example`** to use Supabase config instead of MongoDB
- Now shows: `SUPABASE_URL`, `SUPABASE_KEY`, `USE_SUPABASE=true`

### 4. Cleanup
- **Deleted:** `DEPLOYMENT.md` (superseded by `VERCEL_DEPLOYMENT.md`)
- **Deleted:** `backend/run_migrations.py` (redundant helper)

## Current Schema Structure

### Students Table
```sql
CREATE TABLE public.students (
  id text,
  name text,
  email text,
  register_number text,
  department text,
  course text,
  year text,              -- ← Now TEXT (stores "1st Year", "2nd Year", etc.)
  phone_number text,      -- ← Renamed from 'phone'
  password text,
  registered_events jsonb,
  created_at timestamptz,
  updated_at timestamptz,
  metadata jsonb
);
```

### Other Tables
- **events:** Includes created_by, event_name, start_time/end_time
- **attendance:** student_id + event_id links (with CASCADE delete)
- **unauthorized_logs:** QR token tracking with scanned_at timestamp

## MongoDB Data Mapping

| MongoDB Field | Supabase Type | Notes |
|---|---|---|
| `_id` | `id` (text) | Converted to string |
| `phone` | `phone_number` (text) | Field renamed during migration |
| `year` | `year` (text) | Stored as "1st Year", "2nd Year", etc. |
| `registered_events` | `registered_events` (jsonb) | Array of event IDs |
| `created_at`/`updated_at` | `timestamptz` | Converted to ISO format |

## Files Ready for Migration

1. **Setup Schema:**
   - Run `backend/supabase_reset_schema.sql` in Supabase SQL Editor (drops + recreates)
   - OR run `backend/supabase_schema.sql` (creates if not exists)

2. **Migrate Data:**
   ```bash
   cd backend
   python migrate_to_supabase.py
   ```

3. **Verify:**
   ```sql
   SELECT COUNT(*) FROM students;  -- Should show 5 records
   SELECT COUNT(*) FROM events;    -- Should show 6 records
   SELECT year FROM students LIMIT 1;  -- Should show "1st Year" or similar
   ```

## Data Type Compatibility Check

✅ All data types now match between MongoDB and Supabase schema
✅ Field transformations properly handle text-to-text conversions
✅ Timestamp conversions to ISO 8601 format
✅ Array fields stored as JSONB

## Next Steps

Execute in Supabase:
```sql
-- Copy from backend/supabase_reset_schema.sql
DROP TABLE IF EXISTS attendance CASCADE;
DROP TABLE IF EXISTS unauthorized_logs CASCADE;
DROP TABLE IF EXISTS events CASCADE;
DROP TABLE IF EXISTS students CASCADE;

-- Then run the CREATE TABLE statements...
```

Then run migration script as shown above.
