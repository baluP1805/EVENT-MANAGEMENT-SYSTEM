from config import Config

# Initialize Mongo only when Supabase is not in use
if not Config.USE_SUPABASE and Config.MONGO_URI:
	from pymongo import MongoClient
	client = MongoClient(Config.MONGO_URI)
	db = client[Config.DATABASE_NAME]

	# Collections
	students_collection = db['students']
	events_collection = db['events']
	attendance_collection = db['attendance']
	unauthorized_logs_collection = db['unauthorized_logs']

	# Create indexes for better performance
	students_collection.create_index('email', unique=True)
	students_collection.create_index('register_number', unique=True)
	events_collection.create_index('event_name')
	attendance_collection.create_index([('student_id', 1), ('event_id', 1)])
else:
	# When using Supabase we don't create Mongo collections; keep names defined to avoid NameError
	students_collection = None
	events_collection = None
	attendance_collection = None
	unauthorized_logs_collection = None
