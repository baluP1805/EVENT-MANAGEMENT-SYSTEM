-- Reset Supabase tables for College EMS
-- Run this to drop existing tables and recreate with full schema

-- Drop existing tables (if they exist)
DROP TABLE IF EXISTS public.attendance CASCADE;
DROP TABLE IF EXISTS public.unauthorized_logs CASCADE;
DROP TABLE IF EXISTS public.events CASCADE;
DROP TABLE IF EXISTS public.students CASCADE;

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create tables with full schema
-- Students table
CREATE TABLE public.students (
  id text PRIMARY KEY DEFAULT gen_random_uuid()::text,
  name text,
  email text UNIQUE,
  register_number text UNIQUE,
  department text,
  course text,
  year text,
  phone_number text,
  password text,
  registered_events jsonb DEFAULT '[]'::jsonb,
  created_at timestamptz,
  updated_at timestamptz,
  CONSTRAINT registered_events_is_array CHECK (jsonb_typeof(registered_events) = 'array')
);

-- Events table
CREATE TABLE public.events (
  id text PRIMARY KEY DEFAULT gen_random_uuid()::text,
  event_name text,
  description text,
  date text,
  venue text,
  max_participants integer,
  total_registered integer DEFAULT 0,
  created_at timestamptz,
  updated_at timestamptz
);

-- Attendance table
CREATE TABLE public.attendance (
  id text PRIMARY KEY DEFAULT gen_random_uuid()::text,
  student_id text REFERENCES public.students(id) ON DELETE CASCADE,
  event_id text REFERENCES public.events(id) ON DELETE CASCADE,
  qr_token text,
  marked_at timestamptz,
  status text
);

-- Unauthorized logs table
CREATE TABLE public.unauthorized_logs (
  id text PRIMARY KEY DEFAULT gen_random_uuid()::text,
  qr_token text,
  ip_address text,
  user_agent text,
  scan_data jsonb,
  scanned_at timestamptz,
  status text
);

-- Create indexes for performance
CREATE INDEX idx_students_email ON public.students(email);
CREATE INDEX idx_students_register_number ON public.students(register_number);
CREATE INDEX idx_events_event_name ON public.events(event_name);
CREATE INDEX idx_attendance_student_event ON public.attendance(student_id, event_id);
CREATE INDEX idx_attendance_event ON public.attendance(event_id);
CREATE INDEX idx_unauthorized_logs_scanned_at ON public.unauthorized_logs(scanned_at);

-- Seed default events
INSERT INTO public.events (event_name, description, date, venue, max_participants, total_registered, created_at, updated_at)
VALUES 
  ('Paper Presentation', 'Present your research and technical papers', '2026-03-15', 'Main Auditorium', 100, 0, NOW(), NOW()),
  ('Coding Contest', 'Competitive programming challenge', '2026-03-16', 'Computer Lab A', 150, 0, NOW(), NOW()),
  ('Gaming Tournament', 'E-sports competition', '2026-03-17', 'Gaming Arena', 80, 0, NOW(), NOW()),
  ('Technical Quiz', 'Technology and science quiz competition', '2026-03-18', 'Seminar Hall', 120, 0, NOW(), NOW()),
  ('Project Expo', 'Showcase your innovative projects', '2026-03-19', 'Exhibition Hall', 200, 0, NOW(), NOW()),
  ('Debugging Challenge', 'Find and fix bugs in code', '2026-03-20', 'Computer Lab B', 100, 0, NOW(), NOW());

-- Verify setup
SELECT 'Schema reset completed successfully!' as status;
SELECT COUNT(*) as total_events FROM public.events;
