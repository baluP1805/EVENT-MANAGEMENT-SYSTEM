import qrcode
import io
import base64
import secrets
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont
import json

class QRGenerator:
    @staticmethod
    def generate_qr_token():
        """Generate a secure random token for QR code"""
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def create_qr_data(event_id, event_name, secure_token):
        """Create QR code data payload with event identifier"""
        qr_data = {
            'event_id': str(event_id),
            'event_name': event_name,
            'secure_token': secure_token,
            'timestamp': datetime.utcnow().isoformat(),
            'expiry': (datetime.utcnow() + timedelta(hours=24)).isoformat(),
            'type': 'COLLEGE_EMS_EVENT'
        }
        return json.dumps(qr_data)
    
    @staticmethod
    def create_logo():
        """Create a simple EMS logo for QR code center"""
        # Create circular logo with gradient
        size = 80
        logo = Image.new('RGB', (size, size), '#FFFFFF')
        draw = ImageDraw.Draw(logo)
        
        # Draw outer circle (border)
        draw.ellipse([0, 0, size-1, size-1], fill='#667eea', outline='#764ba2', width=3)
        
        # Draw inner circle
        draw.ellipse([8, 8, size-9, size-9], fill='#FFFFFF')
        
        # Draw text "EMS"
        try:
            # Try to use a nice font, fallback to default if not available
            font = ImageFont.truetype("arial.ttf", 22)
        except:
            font = ImageFont.load_default()
        
        text = "EMS"
        # Get text bounding box
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Center the text
        x = (size - text_width) // 2
        y = (size - text_height) // 2 - 5
        
        draw.text((x, y), text, fill='#667eea', font=font)
        
        return logo
    
    @staticmethod
    def generate_qr_code(event_id, event_name=None):
        """Generate QR code image for an event with embedded logo"""
        from models.event import Event
        
        # If event_name not provided, fetch it
        if not event_name:
            event = Event.find_by_id(event_id)
            if event:
                event_name = event.get('event_name', 'Event')
            else:
                event_name = 'Event'
        
        # Generate secure token
        secure_token = QRGenerator.generate_qr_token()
        
        # Create QR data
        qr_data = QRGenerator.create_qr_data(event_id, event_name, secure_token)
        
        # Generate QR code with high error correction to accommodate logo
        qr = qrcode.QRCode(
            version=2,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        # Create QR code image
        qr_img = qr.make_image(fill_color="#000000", back_color="#FFFFFF").convert('RGB')
        
        # Create and add logo
        logo = QRGenerator.create_logo()
        
        # Calculate position to center the logo
        qr_width, qr_height = qr_img.size
        logo_size = 80
        logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
        
        # Calculate center position
        pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
        
        # Paste logo onto QR code
        qr_img.paste(logo, pos)
        
        # Convert to base64 for easy transmission
        buffer = io.BytesIO()
        qr_img.save(buffer, format='PNG')
        buffer.seek(0)
        img_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        return {
            'qr_image': f'data:image/png;base64,{img_base64}',
            'qr_data': qr_data,
            'secure_token': secure_token,
            'event_name': event_name
        }
    
    @staticmethod
    def verify_qr_data(qr_data_str):
        """Verify and parse QR code data with enhanced validation"""
        try:
            qr_data = json.loads(qr_data_str)
            
            # Validate QR code type
            if qr_data.get('type') != 'COLLEGE_EMS_EVENT':
                return None, 'Invalid QR code. Not a College EMS event QR code.'
            
            # Check required fields
            required_fields = ['event_id', 'event_name', 'secure_token', 'expiry']
            for field in required_fields:
                if field not in qr_data:
                    return None, f'Invalid QR code format. Missing: {field}'
            
            # Check if QR code has expired
            expiry = datetime.fromisoformat(qr_data['expiry'])
            if datetime.utcnow() > expiry:
                return None, f'QR code has expired for event: {qr_data.get("event_name", "Unknown")}'
            
            return qr_data, None
        except json.JSONDecodeError:
            return None, 'Invalid QR code format. Unable to parse data.'
        except (KeyError, ValueError) as e:
            return None, f'Invalid QR code data: {str(e)}'
