"""
NFT Badge Generator
Creates colorful NFT badges for certificates using Pillow
"""

from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime

class NFTGenerator:
    """
    Generates NFT badges for certificates
    
    Features:
    - Colorful design based on certificate type
    - Student name and achievement
    - Unique NFT ID
    - Blockchain hash reference
    """
    
    def __init__(self, output_dir='static/nft_badges'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Color schemes for different certificate types
        self.color_schemes = {
            'Completion': {
                'bg': (52, 152, 219),  # Blue
                'accent': (41, 128, 185),
                'text': (255, 255, 255)
            },
            'Achievement': {
                'bg': (46, 204, 113),  # Green
                'accent': (39, 174, 96),
                'text': (255, 255, 255)
            },
            'Excellence': {
                'bg': (155, 89, 182),  # Purple
                'accent': (142, 68, 173),
                'text': (255, 255, 255)
            },
            'Participation': {
                'bg': (230, 126, 34),  # Orange
                'accent': (211, 84, 0),
                'text': (255, 255, 255)
            }
        }
    
    def create_nft_badge(self, certificate_id, student_name, certificate_type, course, blockchain_hash):
        """
        Create an NFT badge image
        
        Args:
            certificate_id: Unique certificate identifier
            student_name: Name of the student
            certificate_type: Type of certificate
            course: Course name
            blockchain_hash: Blockchain hash for verification
        
        Returns:
            Dictionary with NFT metadata
        """
        # Get color scheme
        colors = self.color_schemes.get(certificate_type, self.color_schemes['Completion'])
        
        # Create image (800x600)
        width, height = 800, 600
        img = Image.new('RGB', (width, height), color=colors['bg'])
        draw = ImageDraw.Draw(img)
        
        # Draw accent border
        border_width = 20
        draw.rectangle(
            [border_width, border_width, width - border_width, height - border_width],
            outline=colors['accent'],
            width=10
        )
        
        # Try to use a better font, fallback to default
        try:
            title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
            name_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
            detail_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
            small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
        except:
            title_font = ImageFont.load_default()
            name_font = ImageFont.load_default()
            detail_font = ImageFont.load_default()
            small_font = ImageFont.load_default()
        
        # Draw "NFT BADGE" at top
        badge_text = "🏆 NFT BADGE 🏆"
        bbox = draw.textbbox((0, 0), badge_text, font=title_font)
        text_width = bbox[2] - bbox[0]
        draw.text(((width - text_width) / 2, 60), badge_text, fill=colors['text'], font=title_font)
        
        # Draw certificate type
        type_text = f"Certificate of {certificate_type}"
        bbox = draw.textbbox((0, 0), type_text, font=name_font)
        text_width = bbox[2] - bbox[0]
        draw.text(((width - text_width) / 2, 140), type_text, fill=colors['text'], font=name_font)
        
        # Draw separator line
        draw.line([(150, 200), (650, 200)], fill=colors['text'], width=3)
        
        # Draw student name
        name_text = f"Awarded to: {student_name}"
        bbox = draw.textbbox((0, 0), name_text, font=detail_font)
        text_width = bbox[2] - bbox[0]
        draw.text(((width - text_width) / 2, 240), name_text, fill=colors['text'], font=detail_font)
        
        # Draw course
        course_text = f"Course: {course}"
        bbox = draw.textbbox((0, 0), course_text, font=detail_font)
        text_width = bbox[2] - bbox[0]
        draw.text(((width - text_width) / 2, 290), course_text, fill=colors['text'], font=detail_font)
        
        # Draw NFT ID
        nft_id = f"NFT-{certificate_id}"
        bbox = draw.textbbox((0, 0), nft_id, font=detail_font)
        text_width = bbox[2] - bbox[0]
        draw.text(((width - text_width) / 2, 360), nft_id, fill=colors['text'], font=detail_font)
        
        # Draw blockchain hash (truncated)
        hash_text = f"Hash: {blockchain_hash[:32]}..."
        bbox = draw.textbbox((0, 0), hash_text, font=small_font)
        text_width = bbox[2] - bbox[0]
        draw.text(((width - text_width) / 2, 420), hash_text, fill=colors['text'], font=small_font)
        
        # Draw verification note
        verify_text = "✓ Verified on EduChain AI+ Blockchain"
        bbox = draw.textbbox((0, 0), verify_text, font=small_font)
        text_width = bbox[2] - bbox[0]
        draw.text(((width - text_width) / 2, 500), verify_text, fill=colors['text'], font=small_font)
        
        # Save image
        filename = f"{certificate_id}_nft.png"
        filepath = os.path.join(self.output_dir, filename)
        img.save(filepath)
        
        # Create NFT metadata
        nft_metadata = {
            'nft_id': f"NFT-{certificate_id}",
            'certificate_id': certificate_id,
            'image_path': f"/static/nft_badges/{filename}",
            'owner_wallet': None,  # Set when issuing
            'blockchain_hash': blockchain_hash,
            'created_at': datetime.now().isoformat(),
            'metadata': {
                'name': f"{certificate_type} Certificate NFT",
                'description': f"NFT Badge for {student_name}'s {certificate_type} certificate in {course}",
                'attributes': [
                    {'trait_type': 'Certificate Type', 'value': certificate_type},
                    {'trait_type': 'Course', 'value': course},
                    {'trait_type': 'Student', 'value': student_name}
                ]
            }
        }
        
        return nft_metadata

# IPFS INTEGRATION NOTES:
# For production with IPFS (decentralized storage):
# 1. Install ipfshttpclient: pip install ipfshttpclient
# 2. Upload image to IPFS: client.add(filepath)
# 3. Store IPFS hash (CID) instead of local path
# 4. NFT metadata should reference: ipfs://{CID}
# 5. Pin important files to ensure availability
