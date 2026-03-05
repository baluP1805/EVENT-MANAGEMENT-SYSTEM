# Events Table Verification Guide

## After Running Migration Script

### 1. Verify Events Table Structure
Run this query in Supabase SQL Editor:
```sql
SELECT 
  column_name, 
  data_type, 
  is_nullable,
  column_default
FROM information_schema.columns
WHERE table_name = 'events'
ORDER BY ordinal_position;
```

**Expected columns:**
- `id` (text, primary key)
- `event_name` (text)
- `description` (text)
- `date` (text)
- `venue` (text)
- `max_participants` (integer)
- `total_registered` (integer, default: 0)
- `created_at` (timestamp with time zone)
- `updated_at` (timestamp with time zone)

### 2. Check Default Events
```sql
SELECT 
  event_name,
  date,
  venue,
  max_participants,
  total_registered
FROM public.events
ORDER BY date;
```

**Expected 6 events:**
1. Paper Presentation (2026-03-15, Main Auditorium, 100)
2. Coding Contest (2026-03-16, Computer Lab A, 150)
3. Gaming Tournament (2026-03-17, Gaming Arena, 80)
4. Technical Quiz (2026-03-18, Seminar Hall, 120)
5. Project Expo (2026-03-19, Exhibition Hall, 200)
6. Debugging Challenge (2026-03-20, Computer Lab B, 100)

### 3. Verify No Missing Data
```sql
-- Check for events with missing required fields
SELECT 
  id,
  event_name,
  CASE WHEN date IS NULL OR date = '' THEN 'MISSING' ELSE date END as date_status,
  CASE WHEN venue IS NULL OR venue = '' THEN 'MISSING' ELSE venue END as venue_status,
  CASE WHEN total_registered IS NULL THEN 'MISSING' ELSE total_registered::text END as registered_status
FROM public.events
WHERE date IS NULL OR date = '' 
   OR venue IS NULL OR venue = ''
   OR total_registered IS NULL;
```

**Expected result:** Empty (no rows) - all events should have required fields

### 4. Test Admin Dashboard
1. Login to admin dashboard
2. Check that events display correctly with:
   - Event names
   - Dates in readable format
   - Venues
   - Registration counts
   - No errors in browser console

### 5. Test Student Events Page
1. Login as student
2. Navigate to Events page
3. Verify all events show:
   - Event name
   - Description
   - Date
   - Venue
   - Can select an event

### Common Issues & Solutions

#### Issue: Events table exists but has old schema
**Solution:** Run `backend/supabase_migration.sql` in Supabase SQL Editor

#### Issue: No events showing in application
**Solution:** 
```sql
-- Manually insert default events
INSERT INTO public.events (event_name, description, date, venue, max_participants, total_registered, created_at, updated_at)
VALUES 
  ('Paper Presentation', 'Present your research and technical papers', '2026-03-15', 'Main Auditorium', 100, 0, NOW(), NOW()),
  ('Coding Contest', 'Competitive programming challenge', '2026-03-16', 'Computer Lab A', 150, 0, NOW(), NOW()),
  ('Gaming Tournament', 'E-sports competition', '2026-03-17', 'Gaming Arena', 80, 0, NOW(), NOW()),
  ('Technical Quiz', 'Technology and science quiz competition', '2026-03-18', 'Seminar Hall', 120, 0, NOW(), NOW()),
  ('Project Expo', 'Showcase your innovative projects', '2026-03-19', 'Exhibition Hall', 200, 0, NOW(), NOW()),
  ('Debugging Challenge', 'Find and fix bugs in code', '2026-03-20', 'Computer Lab B', 100, 0, NOW(), NOW());
```

#### Issue: Application still showing errors
**Solution:**
1. Check that backend is using Supabase (`USE_SUPABASE=true` in `.env`)
2. Verify Supabase connection string is correct
3. Restart the Flask backend
4. Clear browser cache and reload

## API Endpoints Test

### Get All Events (Student)
```bash
GET /api/student/events
```

### Get Dashboard (Admin)
```bash
GET /api/admin/dashboard
Authorization: Bearer {admin_token}
```

Both should return events with `date` and `venue` fields without errors.
