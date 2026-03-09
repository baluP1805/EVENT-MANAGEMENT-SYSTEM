import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import Config
import logging

logger = logging.getLogger(__name__)

class EmailService:
    @staticmethod
    def send_email(to_email, subject, body, html_body=None):
        """Send email notification"""
        try:
            # Check if email is configured
            if not Config.MAIL_USERNAME or not Config.MAIL_PASSWORD:
                logger.info('Email service not configured. Skipping email notification.')
                return False
            
            # Skip if using placeholder values
            if Config.MAIL_USERNAME == 'your-email@gmail.com' or Config.MAIL_PASSWORD == 'your-app-password':
                logger.info('Email service using placeholder credentials. Skipping email notification.')
                return False
            
            # Create message
            msg = MIMEMultipart('alternative')
            # From must match the authenticated Gmail account to avoid SMTPSenderRefused
            msg['From'] = f"College EMS <{Config.MAIL_USERNAME}>"
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Add plain text part
            text_part = MIMEText(body, 'plain')
            msg.attach(text_part)
            
            # Add HTML part if provided
            if html_body:
                html_part = MIMEText(html_body, 'html')
                msg.attach(html_part)
            
            # Send email
            with smtplib.SMTP(Config.MAIL_SERVER, Config.MAIL_PORT) as server:
                server.starttls()
                server.login(Config.MAIL_USERNAME, Config.MAIL_PASSWORD)
                server.send_message(msg)
            logger.info(f'Email sent successfully to {to_email}')
            return True
                
        except smtplib.SMTPAuthenticationError:
            logger.warning('Email authentication failed. Please use Gmail App Password. See setup guide for help.')
            return False
        except Exception as e:
            logger.warning(f'Email service unavailable: {str(e)}')
            return False
    
    @staticmethod
    def send_attendance_confirmation(student_email, student_name, event_name):
        """Send attendance confirmation email"""
        subject = f'Attendance Confirmed - {event_name}'
        
        body = f"""
Dear {student_name},

Your attendance has been successfully recorded for the event: {event_name}

Thank you for participating!

Best regards,
College Event Management System
        """
        
        html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background-color: #4CAF50; color: white; padding: 20px; text-align: center; }}
        .content {{ padding: 20px; background-color: #f9f9f9; }}
        .footer {{ text-align: center; padding: 10px; color: #666; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>Attendance Confirmed ✓</h2>
        </div>
        <div class="content">
            <p>Dear <strong>{student_name}</strong>,</p>
            <p>Your attendance has been successfully recorded for:</p>
            <p style="text-align: center; font-size: 18px; color: #4CAF50;">
                <strong>{event_name}</strong>
            </p>
            <p>Thank you for participating!</p>
        </div>
        <div class="footer">
            <p>College Event Management System</p>
        </div>
    </div>
</body>
</html>
        """
        
        return EmailService.send_email(student_email, subject, body, html_body)

    @staticmethod
    def send_welcome_email(student_email, student_name, register_number):
        """Send welcome email on successful student account registration"""
        subject = 'Welcome to College Event Management System!'

        body = f"""
Dear {student_name},

Welcome to the College Event Management System!

Your account has been successfully created. Here are your details:

  Name           : {student_name}
  Register Number: {register_number}
  Email          : {student_email}

You can now log in and register for upcoming college events.

Login here: http://localhost:5000/pages/login.html

If you did not create this account, please contact the administrator immediately.

Best regards,
College Event Management System
        """

        html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px 20px; text-align: center; border-radius: 8px 8px 0 0; }}
        .header h2 {{ margin: 0; font-size: 24px; }}
        .header p {{ margin: 5px 0 0; opacity: 0.9; font-size: 14px; }}
        .content {{ padding: 30px 20px; background-color: #ffffff; border: 1px solid #e0e0e0; }}
        .details-box {{ background: #f5f7ff; border-left: 4px solid #667eea; padding: 15px 20px; border-radius: 0 4px 4px 0; margin: 20px 0; }}
        .details-box table {{ width: 100%; border-collapse: collapse; }}
        .details-box td {{ padding: 6px 0; font-size: 14px; }}
        .details-box td:first-child {{ color: #666; width: 140px; font-weight: bold; }}
        .btn {{ display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 12px 30px; border-radius: 25px; text-decoration: none; font-weight: bold; margin: 15px 0; }}
        .footer {{ text-align: center; padding: 15px 10px; color: #999; font-size: 12px; background: #f9f9f9; border-radius: 0 0 8px 8px; border: 1px solid #e0e0e0; border-top: none; }}
        .warning {{ font-size: 12px; color: #999; margin-top: 20px; padding-top: 15px; border-top: 1px solid #eee; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>🎓 Welcome to College EMS!</h2>
            <p>Your account is ready</p>
        </div>
        <div class="content">
            <p>Dear <strong>{student_name}</strong>,</p>
            <p>Your account has been successfully created in the <strong>College Event Management System</strong>. You can now participate in exciting college events!</p>
            <div class="details-box">
                <table>
                    <tr><td>Name</td><td>{student_name}</td></tr>
                    <tr><td>Register Number</td><td>{register_number}</td></tr>
                    <tr><td>Email</td><td>{student_email}</td></tr>
                </table>
            </div>
            <p>Click the button below to log in and explore upcoming events:</p>
            <div style="text-align: center;">
                <a href="http://localhost:5000/pages/login.html" class="btn">Login Now →</a>
            </div>
            <p class="warning">⚠️ If you did not create this account, please contact your college administrator immediately.</p>
        </div>
        <div class="footer">
            <p>College Event Management System &nbsp;|&nbsp; Do not reply to this email</p>
        </div>
    </div>
</body>
</html>
        """

        return EmailService.send_email(student_email, subject, body, html_body)

    @staticmethod
    def send_registration_confirmation(student_email, student_name, events):
        """Send event registration confirmation email"""
        subject = 'Event Registration Confirmation'
        
        events_list = '\n'.join([f'- {event}' for event in events])
        
        body = f"""
Dear {student_name},

You have successfully registered for the following events:

{events_list}

We look forward to your participation!

Best regards,
College Event Management System
        """
        
        events_html = ''.join([f'<li>{event}</li>' for event in events])
        
        html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background-color: #2196F3; color: white; padding: 20px; text-align: center; }}
        .content {{ padding: 20px; background-color: #f9f9f9; }}
        .footer {{ text-align: center; padding: 10px; color: #666; font-size: 12px; }}
        ul {{ list-style-type: none; padding: 0; }}
        li {{ padding: 5px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>Registration Successful 🎉</h2>
        </div>
        <div class="content">
            <p>Dear <strong>{student_name}</strong>,</p>
            <p>You have successfully registered for the following events:</p>
            <ul>
                {events_html}
            </ul>
            <p>We look forward to your participation!</p>
        </div>
        <div class="footer">
            <p>College Event Management System</p>
        </div>
    </div>
</body>
</html>
        """
        
        return EmailService.send_email(student_email, subject, body, html_body)
