# Email Configuration Guide

## Quick Start (Skip Emails)

The application **works perfectly without email configuration**! Event registrations and attendance marking will succeed, but confirmation emails won't be sent.

To disable email warnings:
- Leave the default values in `.env`: `MAIL_USERNAME=your-email@gmail.com`
- The app will skip email sending automatically

---

## Gmail Setup (Recommended)

### Prerequisites
- A Gmail account with 2-Step Verification enabled

### Steps to Get Gmail App Password

1. **Enable 2-Step Verification**
   - Go to [Google Account Security](https://myaccount.google.com/security)
   - Click on "2-Step Verification"
   - Follow the setup wizard to enable it

2. **Generate App Password**
   - Go to [Google Account Security](https://myaccount.google.com/security)
   - Click on "2-Step Verification"
   - Scroll down to "App passwords" and click it
   - Select app: **Mail**
   - Select device: **Windows Computer** (or Other)
   - Click "Generate"
   - Copy the 16-character password (e.g., `abcd efgh ijkl mnop`)

3. **Update .env File**
   ```env
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USERNAME=youremail@gmail.com
   MAIL_PASSWORD=abcdefghijklmnop
   MAIL_DEFAULT_SENDER=youremail@gmail.com
   ```
   **Note:** Use the app password WITHOUT spaces

4. **Restart the Server**
   - Stop the Flask app (Ctrl+C)
   - Run `start.bat` again

---

## Alternative SMTP Providers

### Outlook/Hotmail
```env
MAIL_SERVER=smtp.office365.com
MAIL_PORT=587
MAIL_USERNAME=youremail@outlook.com
MAIL_PASSWORD=your-password
MAIL_DEFAULT_SENDER=youremail@outlook.com
```

### Yahoo Mail
```env
MAIL_SERVER=smtp.mail.yahoo.com
MAIL_PORT=587
MAIL_USERNAME=youremail@yahoo.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=youremail@yahoo.com
```
**Note:** Yahoo also requires app-specific passwords

### Custom SMTP Server
```env
MAIL_SERVER=mail.yourdomain.com
MAIL_PORT=587
MAIL_USERNAME=noreply@yourdomain.com
MAIL_PASSWORD=your-password
MAIL_DEFAULT_SENDER=noreply@yourdomain.com
```

---

## Troubleshooting

### Error: "Username and Password not accepted"
**Solution:** You're using your regular Gmail password. Please use an **App Password** instead.

### Error: "Email authentication failed"
**Checklist:**
- ✅ 2-Step Verification enabled?
- ✅ Using App Password (not regular password)?
- ✅ Password copied without spaces?
- ✅ Correct email address?
- ✅ Server restarted after changing .env?

### Emails Not Sending (No Error)
**Check:**
1. Is `MAIL_USERNAME` still set to `your-email@gmail.com`? (This disables email)
2. Check logs for "Email service not configured" message
3. Verify .env file is in `backend/` folder

### "Less Secure Apps" Error
**Gmail deprecated this!** Use App Passwords instead.

---

## Testing Email Configuration

### Method 1: Register for Events
1. Create a student account
2. Login and register for an event
3. Check your email for confirmation

### Method 2: Mark Attendance
1. Admin generates QR code
2. Student scans QR code
3. Check your email for attendance confirmation

### Method 3: Check Logs
Look for these messages in the console:
- ✅ **Success:** `Email sent successfully to student@email.com`
- ⚠️ **Skipped:** `Email service not configured. Skipping email notification.`
- ❌ **Error:** `Email authentication failed. Please use Gmail App Password.`

---

## Production Recommendations

1. **Use a Dedicated Email Account**
   - Don't use personal email
   - Create: `noreply@yourdomain.com` or `events@college.edu`

2. **Use Environment-Specific Credentials**
   - Development: Test email account
   - Production: Official college email

3. **Consider Professional SMTP Services**
   - [SendGrid](https://sendgrid.com/) - 100 emails/day free
   - [Mailgun](https://www.mailgun.com/) - 5,000 emails/month free
   - [Amazon SES](https://aws.amazon.com/ses/) - Pay-as-you-go

4. **Set Up SPF/DKIM Records**
   - Prevents emails going to spam
   - Required for custom domains

---

## Security Best Practices

✅ **DO:**
- Use App Passwords for Gmail
- Keep .env file in .gitignore
- Use different credentials for dev/prod
- Rotate passwords regularly

❌ **DON'T:**
- Commit .env file to Git
- Share your App Password
- Use personal email for production
- Hard-code credentials in code

---

## Need Help?

**Application works but emails not sending?**
- This is normal if email isn't configured
- All other features work perfectly

**Want to enable emails?**
- Follow Gmail Setup above
- Takes 5 minutes
- Completely optional

**Still having issues?**
- Check the troubleshooting section
- Verify 2-Step Verification is enabled
- Ensure you're using App Password, not regular password
