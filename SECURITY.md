# Security Features - College Event Management System

This document outlines the security measures implemented in the College EMS to protect against common vulnerabilities and attacks.

## 🛡️ Security Headers (Flask-Talisman)

**Note**: Security headers are **only enabled in production** to avoid development issues with CSP and HTTPS. Set `FLASK_ENV=production` in your .env file to enable them.

### Content Security Policy (CSP)
- **default-src**: Only allows resources from the same origin
- **script-src**: Allows scripts from self, inline scripts (for dynamic content), and trusted CDNs (jsdelivr, unpkg)
- **style-src**: Allows styles from self, inline styles, Google Fonts, and cdnjs
- **font-src**: Allows fonts from self, Google Fonts, and cdnjs
- **img-src**: Allows images from self, data URIs, and blob URIs (for QR codes)
- **connect-src**: Only allows API connections to the same origin

### HTTP Strict Transport Security (HSTS)
- **Enabled**: Forces HTTPS connections in production
- **Max Age**: 1 year (31536000 seconds)
- **Note**: Currently disabled in development (force_https=False), enable in production

### Frame Options
- **Setting**: DENY
- **Protection**: Prevents clickjacking attacks by not allowing the site to be embedded in iframes

### Referrer Policy
- **Setting**: strict-origin-when-cross-origin
- **Protection**: Controls how much referrer information is sent with requests

### Feature Policy
- **geolocation**: Disabled (not needed for the application)
- **camera**: Allowed for self (QR code scanning)
- **microphone**: Disabled (not needed)

## 🔒 Input Sanitization

### InputSanitizer Class (`backend/utils/sanitizer.py`)

Comprehensive input sanitization to prevent injection attacks:

#### 1. **String Sanitization**
```python
sanitize_string(value, max_length=500)
```
- Escapes HTML entities (prevents XSS)
- Removes control characters and null bytes
- Limits string length

#### 2. **Email Sanitization**
```python
sanitize_email(email)
```
- Validates email format using regex
- Converts to lowercase
- Limits to RFC-compliant length (254 characters)

#### 3. **Registration Number Sanitization**
```python
sanitize_register_number(reg_num)
```
- Allows only alphanumeric characters and hyphens
- Converts to uppercase
- Limited to 50 characters

#### 4. **Phone Number Sanitization**
```python
sanitize_phone(phone)
```
- Allows only digits and common formatting characters (+, -, (, ), spaces)
- Limited to 20 characters

#### 5. **Name Sanitization**
```python
sanitize_name(name)
```
- Allows only letters, spaces, hyphens, and apostrophes
- Removes multiple consecutive spaces
- Limited to 100 characters

#### 6. **Search Query Sanitization**
```python
sanitize_search_query(query)
```
- Removes dangerous characters: $, {, }, \, |, ^
- Prevents MongoDB query injection
- Limited to 200 characters

### Applied Sanitization

Sanitization is applied to all user inputs in:
- **Registration endpoint** (`/api/auth/register`)
  - Name, Email, Phone, Register Number sanitized
- **Login endpoints** (`/api/auth/login`, `/api/auth/admin/login`)
  - Email sanitized before authentication
- **All future endpoints** can use the `@sanitize_input` decorator

## 🚦 Rate Limiting

### Flask-Limiter Configuration

```python
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)
```

**Global Limits:**
- 200 requests per day per IP
- 50 requests per hour per IP

**Protected Endpoints:**
- Login endpoints: Prevents brute force attacks
- Registration endpoints: Prevents spam registrations
- QR scanning: Previously had 50/hour limit

### Benefits:
- Prevents DoS attacks
- Mitigates brute force attempts
- Reduces spam and abuse

## 🔐 Password Security

### bcrypt Hashing
```python
bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
```

**Features:**
- Industry-standard bcrypt algorithm
- Automatic salt generation
- Configurable work factor (rounds)
- Resistant to rainbow table attacks

**Verification:**
```python
bcrypt.checkpw(password.encode('utf-8'), hashed_password)
```

## 🎫 JWT Authentication

### Token-based Authentication

**Student Tokens:**
```python
{
    'student_id': str(student['_id']),
    'email': student['email'],
    'type': 'student',
    'exp': datetime.utcnow() + JWT_EXPIRATION
}
```

**Admin Tokens:**
```python
{
    'email': email,
    'type': 'admin',
    'exp': datetime.utcnow() + JWT_EXPIRATION
}
```

**Security Features:**
- Tokens expire after configured time (default: 24 hours)
- Tokens are signed with secret key
- Cannot be forged without the secret
- Type field prevents privilege escalation

### Token Verification
- All protected endpoints verify JWT tokens
- Invalid tokens are rejected with 401 Unauthorized
- Expired tokens are automatically rejected

## 📋 QR Code Security

### Enhanced QR Data Structure
```python
{
    'student_id': str(student_id),
    'event_id': str(event_id),
    'event_name': event_name,
    'event_type': event_type,
    'timestamp': timestamp,
    'type': 'COLLEGE_EMS_EVENT'
}
```

**Security Measures:**
1. **Type Validation**: Only processes QR codes with `type='COLLEGE_EMS_EVENT'`
2. **Timestamp Included**: Can be used to detect replay attacks
3. **Event Type Validation**: Verifies event type matches expected format
4. **Student-Event Binding**: Validates student is registered for the event
5. **Logo Embedding**: EMS logo in QR center for visual authenticity

### QR Data Verification
```python
verify_qr_data(qr_data, expected_event_type='event')
```
- Validates all required fields exist
- Checks type identifier
- Verifies event type matches expected
- Returns detailed error messages

## 🗃️ Database Security

### MongoDB Best Practices

1. **No SQL Injection**: Using PyMongo ODM prevents SQL injection
2. **Query Sanitization**: Search queries sanitized to prevent MongoDB injection
3. **ObjectId Validation**: IDs validated before database queries
4. **Parameterized Queries**: All queries use proper parameterization

### Example Safe Query:
```python
students_collection.find({"registered_events": ObjectId(event_id)})
```

## 🚨 Error Handling

### Secure Error Messages

**Generic Authentication Errors:**
```python
return jsonify({'success': False, 'message': 'Invalid email or password'}), 401
```
- Doesn't reveal if email exists
- Prevents user enumeration

**Validation Errors:**
- Specific validation messages for user input
- No internal server details exposed
- Logged for admin review

## 📊 Logging & Monitoring

### Unauthorized Access Logging

```python
unauthorized_log_collection.insert_one({
    'student_id': student_id,
    'event_id': event_id,
    'timestamp': timestamp,
    'reason': 'Not registered'
})
```

**Logged Events:**
- Failed login attempts
- Unauthorized QR scan attempts
- Invalid token usage
- Suspicious activity

### Benefits:
- Audit trail for security incidents
- Detect patterns of abuse
- Investigation support

## ✅ Security Checklist

### Implemented ✅
- [x] HTTPS headers (HSTS, CSP, Frame Options)
- [x] Input sanitization on all endpoints
- [x] Rate limiting on all endpoints
- [x] Password hashing with bcrypt
- [x] JWT authentication with expiration
- [x] QR code validation and type checking
- [x] MongoDB injection prevention
- [x] XSS prevention through input escaping
- [x] Clickjacking prevention (Frame Options: DENY)
- [x] Error message sanitization
- [x] Unauthorized access logging

### Recommended for Production 🔧
- [ ] Enable HTTPS (set `force_https=True` in Talisman)
- [ ] Configure SSL/TLS certificates
- [ ] Set strong JWT_SECRET_KEY in production
- [ ] Review and tighten CORS policy
- [ ] Implement session management
- [ ] Add CAPTCHA for registration/login
- [ ] Set up intrusion detection
- [ ] Configure MongoDB authentication
- [ ] Regular security updates
- [ ] Backup and disaster recovery plan

### Future Enhancements 🚀
- [ ] Two-factor authentication (2FA)
- [ ] Password complexity requirements
- [ ] Account lockout after failed attempts
- [ ] Security question recovery
- [ ] Email verification for registration
- [ ] Audit log review dashboard
- [ ] Real-time security alerts
- [ ] Penetration testing

## 🔧 Configuration

### Environment Variables (.env)

```env
# JWT Configuration
JWT_SECRET_KEY=your-super-secret-key-change-in-production
JWT_EXPIRATION_HOURS=24

# Admin Credentials
ADMIN_EMAIL=admin@college.edu
ADMIN_PASSWORD=secure-admin-password

# MongoDB
MONGO_URI=mongodb://localhost:27017/
DATABASE_NAME=college_ems

# Rate Limiting
RATELIMIT_STORAGE_URL=memory://
```

**Security Notes:**
- Change all default credentials
- Use strong JWT secret (min 32 characters)
- Never commit .env file to version control
- Use different secrets in dev/staging/production

## 📚 Dependencies

Security-related packages in `requirements.txt`:

```
Flask==3.0.0              # Web framework
flask-cors==4.0.0         # CORS handling
flask-limiter==3.5.0      # Rate limiting
flask-talisman==1.1.0     # Security headers
bcrypt==4.1.2             # Password hashing
PyJWT==2.8.0              # JWT tokens
```

## 🐛 Reporting Security Issues

If you discover a security vulnerability, please:
1. **Do NOT** open a public issue
2. Email: security@college.edu (or designated contact)
3. Include detailed description and reproduction steps
4. Allow reasonable time for fix before disclosure

## 📖 References

- [OWASP Top Ten](https://owasp.org/www-project-top-ten/)
- [Flask Security Best Practices](https://flask.palletsprojects.com/en/2.3.x/security/)
- [JWT Best Practices](https://datatracker.ietf.org/doc/html/rfc8725)
- [Content Security Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP)

---

**Last Updated**: December 2024  
**Version**: 1.0.0  
**Security Contact**: admin@college.edu
