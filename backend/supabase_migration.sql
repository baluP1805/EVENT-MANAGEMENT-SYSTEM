-- Migration script to fix existing Supabase schema
-- Run this in Supabase SQL Editor if you already have tables created
-- This will update the events table to match the application's expectations

-- Add missing columns to events table if they don't exist
DO $$ 
BEGIN
  -- Check and add date column
  IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                 WHERE table_name='events' AND column_name='date') THEN
    ALTER TABLE public.events ADD COLUMN date text;
  END IF;

  -- Check and add venue column
  IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                 WHERE table_name='events' AND column_name='venue') THEN
    ALTER TABLE public.events ADD COLUMN venue text;
  END IF;

  -- Check and add max_participants column
  IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                 WHERE table_name='events' AND column_name='max_participants') THEN
    ALTER TABLE public.events ADD COLUMN max_participants integer;
  END IF;

  -- Check and add total_registered column
  IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                 WHERE table_name='events' AND column_name='total_registered') THEN
    ALTER TABLE public.events ADD COLUMN total_registered integer DEFAULT 0;
  END IF;

  -- Remove old columns if they exist
  IF EXISTS (SELECT 1 FROM information_schema.columns 
             WHERE table_name='events' AND column_name='location') THEN
    -- Migrate data from location to venue
    UPDATE public.events SET venue = location WHERE venue IS NULL;
    ALTER TABLE public.events DROP COLUMN location;
  END IF;

  IF EXISTS (SELECT 1 FROM information_schema.columns 
             WHERE table_name='events' AND column_name='start_time') THEN
    -- Migrate data from start_time to date
    UPDATE public.events SET date = start_time::text WHERE date IS NULL;
    ALTER TABLE public.events DROP COLUMN start_time;
  END IF;

  IF EXISTS (SELECT 1 FROM information_schema.columns 
             WHERE table_name='events' AND column_name='end_time') THEN
    ALTER TABLE public.events DROP COLUMN end_time;
  END IF;

  IF EXISTS (SELECT 1 FROM information_schema.columns 
             WHERE table_name='events' AND column_name='created_by') THEN
    ALTER TABLE public.events DROP COLUMN created_by;
  END IF;

  IF EXISTS (SELECT 1 FROM information_schema.columns 
             WHERE table_name='events' AND column_name='metadata') THEN
    ALTER TABLE public.events DROP COLUMN metadata;
  END IF;

  -- Remove metadata from students if it exists
  IF EXISTS (SELECT 1 FROM information_schema.columns 
             WHERE table_name='students' AND column_name='metadata') THEN
    ALTER TABLE public.students DROP COLUMN metadata;
  END IF;
END $$;

-- Ensure registered_events has a default value
ALTER TABLE public.students ALTER COLUMN registered_events SET DEFAULT '[]'::jsonb;

-- Update all NULL registered_events to empty array
UPDATE public.students SET registered_events = '[]'::jsonb WHERE registered_events IS NULL;

-- Fix any invalid JSONB in registered_events (convert invalid entries to empty array)
UPDATE public.students 
SET registered_events = '[]'::jsonb 
WHERE NOT (registered_events::text ~ '^(\[.*\]|\{.*\})$');

-- Ensure all registered_events are properly formatted JSON arrays
DO $$
DECLARE
  student_record RECORD;
  fixed_events jsonb;
BEGIN
  FOR student_record IN SELECT id, registered_events FROM public.students WHERE registered_events IS NOT NULL
  LOOP
    BEGIN
      -- Try to validate the JSONB, if it fails, reset to empty array
      IF jsonb_typeof(student_record.registered_events) != 'array' THEN
        UPDATE public.students SET registered_events = '[]'::jsonb WHERE id = student_record.id;
      END IF;
    EXCEPTION WHEN OTHERS THEN
      -- If any error occurs, reset to empty array
      UPDATE public.students SET registered_events = '[]'::jsonb WHERE id = student_record.id;
    END;
  END LOOP;
END $$;

-- Initialize total_registered to 0 if NULL
UPDATE public.events SET total_registered = 0 WHERE total_registered IS NULL;

-- Ensure all events have date and venue fields (set defaults if missing)
UPDATE public.events 
SET date = COALESCE(date, created_at::text, '2026-03-15')
WHERE date IS NULL OR date = '';

UPDATE public.events 
SET venue = COALESCE(venue, 'To Be Announced')
WHERE venue IS NULL OR venue = '';

-- Seed default events if table is empty
DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM public.events LIMIT 1) THEN
    INSERT INTO public.events (event_name, description, date, venue, max_participants, total_registered, created_at, updated_at)
    VALUES 
      ('Paper Presentation', 'Present your research and technical papers', '2026-03-15', 'Main Auditorium', 100, 0, NOW(), NOW()),
      ('Coding Contest', 'Competitive programming challenge', '2026-03-16', 'Computer Lab A', 150, 0, NOW(), NOW()),
      ('Gaming Tournament', 'E-sports competition', '2026-03-17', 'Gaming Arena', 80, 0, NOW(), NOW()),
      ('Technical Quiz', 'Technology and science quiz competition', '2026-03-18', 'Seminar Hall', 120, 0, NOW(), NOW()),
      ('Project Expo', 'Showcase your innovative projects', '2026-03-19', 'Exhibition Hall', 200, 0, NOW(), NOW()),
      ('Debugging Challenge', 'Find and fix bugs in code', '2026-03-20', 'Computer Lab B', 100, 0, NOW(), NOW());
  END IF;
END $$;

-- Create indexes if they don't exist
CREATE INDEX IF NOT EXISTS idx_students_email ON public.students(email);
CREATE INDEX IF NOT EXISTS idx_students_register_number ON public.students(register_number);
CREATE INDEX IF NOT EXISTS idx_events_event_name ON public.events(event_name);
CREATE INDEX IF NOT EXISTS idx_attendance_student_event ON public.attendance(student_id, event_id);
CREATE INDEX IF NOT EXISTS idx_attendance_event ON public.attendance(event_id);
CREATE INDEX IF NOT EXISTS idx_unauthorized_logs_scanned_at ON public.unauthorized_logs(scanned_at);

-- Add constraint to ensure registered_events is always an array
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_constraint 
    WHERE conname = 'registered_events_is_array' 
    AND conrelid = 'public.students'::regclass
  ) THEN
    ALTER TABLE public.students 
    ADD CONSTRAINT registered_events_is_array 
    CHECK (jsonb_typeof(registered_events) = 'array');
  END IF;
END $$;

-- Verify schema
SELECT 'Migration completed successfully!' as status;

-- Show any students with invalid registered_events (should be none after migration)
SELECT COUNT(*) as students_with_valid_events 
FROM public.students 
WHERE jsonb_typeof(registered_events) = 'array';
