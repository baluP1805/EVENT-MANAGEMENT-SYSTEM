#!/usr/bin/env python3
"""
Script to connect to MongoDB and inspect the students collection.
"""

from pymongo import MongoClient
import json

# Connect to MongoDB at localhost:27017
try:
    client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000)
    # Test connection
    client.admin.command('ping')
    print("✓ Successfully connected to MongoDB at localhost:27017\n")
except Exception as e:
    print(f"✗ Failed to connect to MongoDB: {e}")
    exit(1)

# Access the college_ems database and students collection
db = client['college_ems']
students_collection = db['students']

# Get a sample student document
try:
    sample_student = students_collection.find_one()
    if sample_student is None:
        print("✗ No documents found in the students collection")
        exit(1)
    
    print("✓ Sample student document found\n")
    print("Full document:")
    print(json.dumps(sample_student, indent=2, default=str))
    print("\n" + "="*60)
    
    # Get the 'year' field
    if 'year' in sample_student:
        year_value = sample_student['year']
        year_type = type(year_value).__name__
        
        print(f"\n'year' field found:")
        print(f"  Value: {repr(year_value)}")
        print(f"  Type: {year_type}")
        print(f"  Type details: {type(year_value)}")
    else:
        print("\n✗ 'year' field not found in the sample document")
        print("Available fields:", list(sample_student.keys()))
        
        # Check if there are similar fields
        similar_fields = [k for k in sample_student.keys() if 'year' in k.lower()]
        if similar_fields:
            print(f"Similar fields found: {similar_fields}")
            for field in similar_fields:
                val = sample_student[field]
                print(f"  {field}: {repr(val)} (type: {type(val).__name__})")
    
    # Get statistics
    print(f"\n" + "="*60)
    print(f"\nCollection Statistics:")
    print(f"  Total documents in students collection: {students_collection.count_documents({})}")
    
except Exception as e:
    print(f"✗ Error querying collection: {e}")
    exit(1)
finally:
    client.close()
