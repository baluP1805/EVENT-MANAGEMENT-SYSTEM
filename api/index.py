"""
Vercel serverless entry point.
Adds the backend directory to sys.path so all existing imports work unchanged.
"""
import sys
import os

# Make backend package importable from this file's location
backend_dir = os.path.join(os.path.dirname(__file__), '..', 'backend')
sys.path.insert(0, os.path.abspath(backend_dir))

from app import app  # noqa: F401 – Vercel looks for a variable named `app`
