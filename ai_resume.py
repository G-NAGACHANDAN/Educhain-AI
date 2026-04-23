"""
AI Resume Generator
Automatically creates professional resumes from student credentials
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import os
from datetime import datetime

class AIResumeGenerator:
    """
    AI-powered resume generation
    
    Creates professional PDF resumes using:
    - Student credentials
    - Extracted skills
    - Academic performance
    - Certificate history
    - AI-generated summary
    """
    
    def __init__(self, output_dir='static/resumes'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def generate_ai_summary(self, student, certificates):
        """
        Generate AI-powered professional summary
        
        AI Logic:
        - Analyze certificate types and courses
        - Identify strongest skills
        - Create compelling summary paragraph
        """
        name = student.get('name', 'Student')
        skills = student.get('skills', [])
        cert_count = len(certificates)
        
        # Extract unique courses and types
        courses = list(set([cert['certificate'].get('course', '') for cert in certificates]))
        cert_types = list(set([cert['certificate'].get('type', '') for cert in certificates]))
        
        # Count excellence certificates
        excellence_count = sum(1 for cert in certificates if cert['certificate'].get('type') == 'Excellence')
        
        # AI-generated summary
        if excellence_count > 0:
            performance = "high-achieving"
        elif cert_count >= 3:
            performance = "accomplished"
        else:
            performance = "motivated"
        
        # Build summary
        summary = f"{performance.capitalize()} professional with {cert_count} verified credential{'s' if cert_count != 1 else ''} "
        
        if skills:
            top_skills = ', '.join(skills[:3])
            summary += f"demonstrating expertise in {top_skills}. "
        
        if courses:
            summary += f"Completed comprehensive training in {', '.join(courses[:2])}. "
        
        summary += "Proven track record of academic excellence and continuous learning, backed by blockchain-verified credentials on EduChain AI+ platform."
        
        return summary
    
    def generate_resume(self, student, certificates):
        """
        Generate professional PDF resume
        
        Args:
            student: Student wallet data
            certificates: List of certificates from blockchain
        
        Returns:
            Path to generated PDF
        """
        # Create filename
        student_name = student.get('name', 'Student').replace(' ', '_')
        wallet = student.get('wallet_address', 'unknown')
        filename = f"resume_{student_name}_{wallet[:8]}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        
        # Create PDF document
        doc = SimpleDocTemplate(filepath, pagesize=letter,
                               topMargin=0.5*inch, bottomMargin=0.5*inch,
                               leftMargin=0.75*inch, rightMargin=0.75*inch)
        
        # Container for PDF elements
        story = []
        
        # Styles
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=6,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#34495e'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        )
        
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=6
        )
        
        # Name
        name = student.get('name', 'Professional Resume')
        story.append(Paragraph(name.upper(), title_style))
        story.append(Spacer(1, 0.1*inch))
        
        # Contact Info
        contact_info = f"Email: {student.get('email', 'N/A')} | Student ID: {student.get('student_id', 'N/A')}"
        contact_style = ParagraphStyle('Contact', parent=normal_style, alignment=TA_CENTER, fontSize=9)
        story.append(Paragraph(contact_info, contact_style))
        
        # Blockchain verification
        blockchain_text = f"🔒 Blockchain Verified | Wallet: {student.get('wallet_address', 'N/A')}"
        story.append(Paragraph(blockchain_text, contact_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Professional Summary
        story.append(Paragraph("PROFESSIONAL SUMMARY", heading_style))
        summary = self.generate_ai_summary(student, certificates)
        story.append(Paragraph(summary, normal_style))
        story.append(Spacer(1, 0.1*inch))
        
        # Skills
        skills = student.get('skills', [])
        if skills:
            story.append(Paragraph("CORE COMPETENCIES", heading_style))
            # Create skills table (3 columns)
            skill_rows = []
            for i in range(0, len(skills), 3):
                row = ['• ' + skills[i] if i < len(skills) else '',
                       '• ' + skills[i+1] if i+1 < len(skills) else '',
                       '• ' + skills[i+2] if i+2 < len(skills) else '']
                skill_rows.append(row)
            
            skills_table = Table(skill_rows, colWidths=[2.2*inch, 2.2*inch, 2.2*inch])
            skills_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2c3e50')),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ]))
            story.append(skills_table)
            story.append(Spacer(1, 0.1*inch))
        
        # Certifications & Credentials
        if certificates:
            story.append(Paragraph("CERTIFICATIONS & CREDENTIALS", heading_style))
            story.append(Paragraph("All credentials verified on blockchain", 
                                 ParagraphStyle('Subtext', parent=normal_style, fontSize=8, textColor=colors.grey)))
            story.append(Spacer(1, 0.1*inch))
            
            for cert_data in certificates:
                cert = cert_data['certificate']
                
                # Certificate title
                cert_title = f"<b>{cert.get('type', 'Certificate')}: {cert.get('course', 'N/A')}</b>"
                story.append(Paragraph(cert_title, normal_style))
                
                # Certificate details
                grade = cert.get('grade', 'N/A')
                year = cert.get('year', 'N/A')
                details = f"Grade: {grade} | Year: {year} | ID: {cert.get('certificate_id', 'N/A')}"
                detail_style = ParagraphStyle('Details', parent=normal_style, fontSize=8, textColor=colors.grey)
                story.append(Paragraph(details, detail_style))
                
                # Blockchain verification
                block_hash = cert_data.get('block_hash', 'N/A')[:16]
                verify_text = f"✓ Blockchain Hash: {block_hash}..."
                story.append(Paragraph(verify_text, detail_style))
                story.append(Spacer(1, 0.1*inch))
        
        # Footer
        story.append(Spacer(1, 0.3*inch))
        footer_text = f"Generated by EduChain AI+ | {datetime.now().strftime('%B %d, %Y')}"
        footer_style = ParagraphStyle('Footer', parent=normal_style, fontSize=7, 
                                      textColor=colors.grey, alignment=TA_CENTER)
        story.append(Paragraph(footer_text, footer_style))
        story.append(Paragraph("This resume is powered by blockchain technology and AI", footer_style))
        
        # Build PDF
        doc.build(story)
        
        return filepath

# AI ENHANCEMENT IDEAS:
# 1. Parse job descriptions and tailor resume accordingly
# 2. Use NLP to optimize keyword placement for ATS systems
# 3. Generate multiple resume versions for different roles
# 4. Add visual charts/graphs for skill proficiency
# 5. Include AI-generated achievement statements
# 6. Analyze top resumes to learn best practices
