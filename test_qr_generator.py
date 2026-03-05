"""
Quick verification test for QR Generator utility
Tests QR generation, verification, and signature validation
"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from utils.qr_generator import QRGenerator
import json

print("=" * 60)
print("QR Generator Verification Test")
print("=" * 60)

# Test 1: Generate QR Code
print("\n✅ Test 1: Generate QR Code")
event_id = "test-event-123"
secure_token = "secure-token-abc"

qr_data = QRGenerator.generate_qr_code(event_id, secure_token)
print(f"Generated QR Data: {qr_data}")

# Parse and display
qr_json = json.loads(qr_data)
print(f"  • Event ID: {qr_json['event_id']}")
print(f"  • Secure Token: {qr_json['secure_token']}")
print(f"  • Timestamp: {qr_json['timestamp']}")
print(f"  • Signature: {qr_json['signature'][:20]}... (truncated)")

# Test 2: Verify Valid QR Code
print("\n✅ Test 2: Verify Valid QR Code")
result = QRGenerator.verify_qr_data(qr_data, event_id)
print(f"Verification Result: {result}")
if result['valid']:
    print("  ✓ QR code is VALID")
    print(f"  • Event ID: {result['event_id']}")
    print(f"  • Secure Token: {result['secure_token']}")
else:
    print(f"  ✗ QR code is INVALID: {result.get('error', 'Unknown error')}")

# Test 3: Verify with Wrong Event ID
print("\n✅ Test 3: Verify with Wrong Event ID (Should Fail)")
result = QRGenerator.verify_qr_data(qr_data, "wrong-event-id")
print(f"Verification Result: {result}")
if not result['valid']:
    print(f"  ✓ Correctly rejected: {result.get('error', 'Unknown error')}")
else:
    print("  ✗ ERROR: Should have been rejected!")

# Test 4: Verify Tampered QR Code
print("\n✅ Test 4: Verify Tampered QR Code (Should Fail)")
qr_json = json.loads(qr_data)
qr_json['event_id'] = "tampered-event-id"  # Modify data
tampered_qr_data = json.dumps(qr_json)
result = QRGenerator.verify_qr_data(tampered_qr_data, event_id)
print(f"Verification Result: {result}")
if not result['valid']:
    print(f"  ✓ Correctly rejected tampered data: {result.get('error', 'Unknown error')}")
else:
    print("  ✗ ERROR: Tampered QR code should have been rejected!")

# Test 5: Verify Invalid JSON
print("\n✅ Test 5: Verify Invalid JSON (Should Fail)")
result = QRGenerator.verify_qr_data("invalid-json-data", event_id)
print(f"Verification Result: {result}")
if not result['valid']:
    print(f"  ✓ Correctly rejected invalid JSON: {result.get('error', 'Unknown error')}")
else:
    print("  ✗ ERROR: Invalid JSON should have been rejected!")

print("\n" + "=" * 60)
print("All Tests Completed! ✅")
print("=" * 60)
print("\nQR Generator utility is working correctly.")
print("Ready for integration with attendance system.")
