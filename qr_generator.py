"""
QR Code Generator
Creates QR codes for certificate verification
"""

import qrcode
import os

class QRCodeGenerator:
    """
    Generate QR codes for certificate verification
    
    Each QR code links to the public verification page
    """
    
    def __init__(self, output_dir='static/qr_codes', base_url=None):
        self.output_dir = output_dir
        
        # Use Replit domain if available, otherwise localhost
        if base_url is None:
            replit_domain = os.environ.get('REPLIT_DOMAINS', '').split(',')[0].strip()
            if replit_domain:
                self.base_url = f'https://{replit_domain}'
            else:
                self.base_url = 'http://localhost:5000'
        else:
            self.base_url = base_url
            
        os.makedirs(output_dir, exist_ok=True)
    
    def generate_qr(self, certificate_id):
        """
        Generate QR code for certificate verification
        
        Args:
            certificate_id: Unique certificate identifier
        
        Returns:
            Path to QR code image
        """
        # Create verification URL
        verification_url = f"{self.base_url}/verify/{certificate_id}"
        
        # Create QR code
        qr = qrcode.QRCode(
            version=1,  # Controls size (1-40)
            error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction
            box_size=10,
            border=4,
        )
        
        qr.add_data(verification_url)
        qr.make(fit=True)
        
        # Create image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save image
        filename = f"{certificate_id}_qr.png"
        filepath = os.path.join(self.output_dir, filename)
        img.save(filepath)
        
        return f"/static/qr_codes/{filename}"

# QR CODE USAGE:
# 1. Printed on physical certificates
# 2. Embedded in digital certificates
# 3. Shared via email/social media
# 4. Quick verification without typing certificate ID
# 5. Works offline - can be scanned and verified later
