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
    def _get_event_style(event_name):
        """
        Return (ring_color, inner_color, label) based on event name keywords.
        Each category gets a visually distinct color pair and 3-char abbreviation.
        Falls back to a hash-derived color so every event is unique.
        """
        name_upper = event_name.upper()

        # (keywords, ring_color, inner_color, label)
        CATEGORIES = [
            (
                ['TECH', 'CODE', 'HACK', 'PYTHON', 'JAVA', 'WEB', 'APP',
                 'AI', 'ML', 'DATA', 'CLOUD', 'IOT', 'CYBER', 'PROGRAM',
                 'SOFTWARE', 'DIGITAL', 'NETWORK'],
                '#1d4ed8', '#dbeafe', 'TEC'
            ),
            (
                ['SPORT', 'CRICKET', 'FOOTBALL', 'BASKET', 'VOLLEY',
                 'TENNIS', 'RUN', 'SWIM', 'CHESS', 'GAME', 'ATHLET',
                 'BADMINTON', 'KABADDI', 'THROW', 'TRACK'],
                '#15803d', '#dcfce7', 'SPT'
            ),
            (
                ['DANCE', 'MUSIC', 'ARTS', 'ART', 'DRAMA', 'THEATRE',
                 'SING', 'PHOTO', 'CULTUR', 'FILM', 'PAINT', 'SKETCH',
                 'BAND', 'CONCERT', 'PERFORM'],
                '#7e22ce', '#f3e8ff', 'ART'
            ),
            (
                ['SCIENCE', 'PHYSICS', 'CHEM', 'BIO', 'MATH', 'QUIZ',
                 'ASTRO', 'ROBOT', 'INNOV', 'RESEARCH', 'LAB', 'EXPO',
                 'OLYMPIAD', 'ENVIRON'],
                '#0e7490', '#cffafe', 'SCI'
            ),
            (
                ['MANAGE', 'BUSINESS', 'FINANCE', 'MARKET', 'LEADER',
                 'ENTRE', 'MBA', 'ECONO', 'COMMERCE', 'HR', 'STARTUP',
                 'INVEST', 'PITCH'],
                '#c2410c', '#ffedd5', 'MGT'
            ),
            (
                ['WORKSHOP', 'SEMINAR', 'TALK', 'KEYNOTE', 'LECTURE',
                 'TRAIN', 'BOOT', 'CAMP', 'FEST', 'SYMPOSIUM', 'CONFEREN'],
                '#a16207', '#fef9c3', 'WRK'
            ),
        ]

        for keywords, ring, inner, label in CATEGORIES:
            if any(kw in name_upper for kw in keywords):
                return ring, inner, label

        # Hash-based fallback — deterministic & unique per event name
        FALLBACK_PAIRS = [
            ('#dc2626', '#fee2e2'),
            ('#db2777', '#fce7f3'),
            ('#0f766e', '#ccfbf1'),
            ('#4338ca', '#e0e7ff'),
            ('#b45309', '#fef3c7'),
            ('#0369a1', '#e0f2fe'),
        ]
        ring, inner = FALLBACK_PAIRS[abs(hash(event_name)) % len(FALLBACK_PAIRS)]
        label = event_name[:3].upper()
        return ring, inner, label

    @staticmethod
    def create_event_logo(event_name):
        """
        Create an event-themed circular badge for QR code center.
        Design: colored outer ring → light-tinted inner circle → accent dot → 3-char label.
        """
        ring_color, inner_color, label = QRGenerator._get_event_style(event_name)
        size = 80

        logo = Image.new('RGBA', (size, size), (255, 255, 255, 0))
        draw = ImageDraw.Draw(logo)

        # Outer filled circle (ring color)
        draw.ellipse([0, 0, size - 1, size - 1], fill=ring_color)

        # Inner tinted circle
        margin = 7
        draw.ellipse(
            [margin, margin, size - margin - 1, size - margin - 1],
            fill=inner_color
        )

        # Small accent dot (ring color) near top-center
        dot_r = 5
        dot_cx = size // 2
        dot_cy = margin + dot_r + 3
        draw.ellipse(
            [dot_cx - dot_r, dot_cy - dot_r, dot_cx + dot_r, dot_cy + dot_r],
            fill=ring_color
        )

        # 3-char label text
        font = None
        for font_name in ('arialbd.ttf', 'arial.ttf', 'DejaVuSans-Bold.ttf',
                          'DejaVuSans.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'):
            try:
                font = ImageFont.truetype(font_name, 18)
                break
            except Exception:
                continue
        if font is None:
            font = ImageFont.load_default()

        bbox = draw.textbbox((0, 0), label, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        tx = (size - tw) // 2
        ty = size // 2 - th // 2 + 4   # shift slightly below center to avoid the dot
        draw.text((tx, ty), label, fill=ring_color, font=font)

        # Flatten RGBA → RGB with white background for paste compatibility
        bg = Image.new('RGB', (size, size), '#FFFFFF')
        if logo.mode == 'RGBA':
            bg.paste(logo, mask=logo.split()[3])
        else:
            bg.paste(logo)
        return bg

    @staticmethod
    def generate_qr_code(event_id, event_name=None):
        """Generate QR code image for an event with an event-themed center logo.

        Uses ERROR_CORRECT_H (≤30% obscured) so the embedded logo never
        prevents scanning.
        """
        from models.event import Event

        if not event_name:
            event = Event.find_by_id(event_id)
            event_name = event.get('event_name', 'Event') if event else 'Event'

        secure_token = QRGenerator.generate_qr_token()
        qr_data = QRGenerator.create_qr_data(event_id, event_name, secure_token)

        qr = qrcode.QRCode(
            version=2,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)

        qr_img = qr.make_image(fill_color='#000000', back_color='#FFFFFF').convert('RGB')

        logo = QRGenerator.create_event_logo(event_name)
        logo_size = 80
        logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)

        qr_width, qr_height = qr_img.size
        pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
        qr_img.paste(logo, pos)

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
