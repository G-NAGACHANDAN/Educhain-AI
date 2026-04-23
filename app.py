"""
EduChain AI+ - Main Flask Application
A blockchain and AI-powered credential verification platform
"""

from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import os
import json
from datetime import datetime

# Import custom modules
from blockchain import Blockchain, Block
from wallet import WalletManager
from nft_generator import NFTGenerator
from ai_skills import AISkillExtractor
from ai_resume import AIResumeGenerator
from ai_jobs import AIJobMatcher
from ai_chatbot import AIChatbot
from qr_generator import QRCodeGenerator

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SESSION_SECRET', 'dev-secret-key-change-in-production')
CORS(app)

# Initialize blockchain and components
blockchain = Blockchain()
wallet_manager = WalletManager()
nft_generator = NFTGenerator()
skill_extractor = AISkillExtractor()
resume_generator = AIResumeGenerator()
job_matcher = AIJobMatcher()
chatbot = AIChatbot()
qr_generator = QRCodeGenerator()

# Ensure directories exist
os.makedirs('static/nft_badges', exist_ok=True)
os.makedirs('static/qr_codes', exist_ok=True)
os.makedirs('static/resumes', exist_ok=True)
os.makedirs('data', exist_ok=True)

# ==================== ROUTES ====================

@app.route('/')
def index():
    """Home page with platform overview and stats"""
    stats = {
        'total_certificates': len(blockchain.chain) - 1,  # Exclude genesis block
        'total_students': len(wallet_manager.get_student_wallets()),
        'total_skills': len(skill_extractor.get_all_skills()),
        'blockchain_length': len(blockchain.chain)
    }
    return render_template('index.html', stats=stats)

@app.route('/admin')
def admin_dashboard():
    """Admin dashboard for certificate issuance"""
    return render_template('admin.html')

@app.route('/student/<wallet_address>')
def student_dashboard(wallet_address):
    """Student dashboard showing certificates and NFT badges"""
    return render_template('student.html', wallet_address=wallet_address)

@app.route('/verify/<certificate_id>')
def verify_certificate(certificate_id):
    """Public certificate verification page"""
    certificate = blockchain.get_certificate_by_id(certificate_id)
    if certificate:
        return render_template('verify.html', certificate=certificate)
    return render_template('verify.html', error="Certificate not found")

# ==================== API ROUTES ====================

@app.route('/api/register_student', methods=['POST'])
def register_student():
    """Register a new student and create wallet"""
    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 400
    
    data = request.get_json()
    if not data or not isinstance(data, dict):
        return jsonify({'error': 'Request body must be a JSON object'}), 400
    
    name = data.get('name')
    email = data.get('email')
    student_id = data.get('student_id')
    
    if not all([name, email, student_id]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Create student wallet
    wallet = wallet_manager.create_student_wallet(name, email, student_id)
    
    return jsonify({
        'success': True,
        'wallet': wallet
    })

@app.route('/api/create_admin_wallet', methods=['POST'])
def create_admin_wallet():
    """Create an admin wallet for college authority"""
    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 400
    
    data = request.get_json()
    if not data or not isinstance(data, dict):
        return jsonify({'error': 'Request body must be a JSON object'}), 400
    
    institution_name = data.get('institution_name')
    admin_name = data.get('admin_name')
    
    if not all([institution_name, admin_name]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    wallet = wallet_manager.create_admin_wallet(institution_name, admin_name)
    
    return jsonify({
        'success': True,
        'wallet': wallet
    })

@app.route('/api/issue_certificate', methods=['POST'])
def issue_certificate():
    """Issue a new certificate and create NFT badge"""
    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 400
    
    data = request.get_json()
    if not data or not isinstance(data, dict):
        return jsonify({'error': 'Request body must be a JSON object'}), 400
    
    # Extract certificate data
    certificate_type = data.get('certificate_type')
    student_name = data.get('student_name')
    student_wallet = data.get('student_wallet')
    course = data.get('course')
    grade = data.get('grade')
    year = data.get('year')
    admin_wallet = data.get('admin_wallet')
    
    if not all([certificate_type, student_name, student_wallet, course, admin_wallet]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Generate unique certificate ID
    certificate_id = f"CERT-{datetime.now().strftime('%Y%m%d%H%M%S')}-{student_wallet[:8]}"
    
    # Extract skills using AI
    skills = skill_extractor.extract_skills(course, grade, certificate_type)
    
    # Create certificate data
    certificate_data = {
        'certificate_id': certificate_id,
        'type': certificate_type,
        'student_name': student_name,
        'student_wallet': student_wallet,
        'course': course,
        'grade': grade or 'N/A',
        'year': year or datetime.now().year,
        'skills': skills,
        'admin_wallet': admin_wallet,
        'issued_date': datetime.now().isoformat()
    }
    
    # Add to blockchain
    block = blockchain.add_certificate(certificate_data)
    
    # Generate NFT badge
    nft_data = nft_generator.create_nft_badge(
        certificate_id=certificate_id,
        student_name=student_name,
        certificate_type=certificate_type,
        course=course,
        blockchain_hash=block['hash']
    )
    
    # Generate QR code
    qr_path = qr_generator.generate_qr(certificate_id)
    
    # Update student wallet with skills and NFT badge
    wallet_manager.add_skills_to_student(student_wallet, skills)
    wallet_manager.add_nft_to_student(student_wallet, {
        'certificate_id': certificate_id,
        'image_path': nft_data['image_path'],
        'certificate_type': certificate_type,
        'course': course,
        'issued_date': datetime.now().isoformat()
    })
    
    # Increment admin's certificate issuance count
    wallet_manager.increment_admin_issuance(admin_wallet)
    
    return jsonify({
        'success': True,
        'certificate_id': certificate_id,
        'block_hash': block['hash'],
        'nft_badge': nft_data['image_path'],
        'qr_code': qr_path,
        'skills_extracted': skills
    })

@app.route('/api/verify_certificate/<certificate_id>', methods=['GET'])
def api_verify_certificate(certificate_id):
    """API endpoint to verify certificate authenticity"""
    certificate = blockchain.get_certificate_by_id(certificate_id)
    
    if not certificate:
        return jsonify({'error': 'Certificate not found', 'verified': False}), 404
    
    # Verify blockchain integrity
    is_valid = blockchain.is_chain_valid()
    
    return jsonify({
        'verified': is_valid,
        'certificate': certificate,
        'blockchain_valid': is_valid,
        'trust_score': 100 if is_valid else 0
    })

@app.route('/api/student_certificates/<wallet_address>', methods=['GET'])
def get_student_certificates(wallet_address):
    """Get all certificates for a student"""
    certificates = blockchain.get_certificates_by_wallet(wallet_address)
    return jsonify({'certificates': certificates})

@app.route('/api/ai_extract_skills', methods=['POST'])
def ai_extract_skills():
    """Extract skills from course/certificate data"""
    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 400
    
    data = request.get_json()
    if not data or not isinstance(data, dict):
        return jsonify({'error': 'Request body must be a JSON object'}), 400
    
    course = data.get('course', '')
    grade = data.get('grade', '')
    cert_type = data.get('certificate_type', '')
    
    skills = skill_extractor.extract_skills(course, grade, cert_type)
    return jsonify({'skills': skills})

@app.route('/api/generate_resume/<wallet_address>', methods=['GET'])
def generate_resume(wallet_address):
    """Generate AI-powered resume for a student"""
    # Get student data
    student = wallet_manager.get_student_by_wallet(wallet_address)
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    
    # Get certificates
    certificates = blockchain.get_certificates_by_wallet(wallet_address)
    
    # Generate resume
    resume_path = resume_generator.generate_resume(student, certificates)
    
    return send_file(resume_path, as_attachment=True)

@app.route('/api/recommend_jobs/<wallet_address>', methods=['GET'])
def recommend_jobs(wallet_address):
    """Get AI-powered job recommendations"""
    student = wallet_manager.get_student_by_wallet(wallet_address)
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    
    recommendations = job_matcher.match_jobs(student['skills'])
    
    return jsonify({'recommendations': recommendations})

@app.route('/api/chatbot_query', methods=['POST'])
def chatbot_query():
    """Process chatbot queries"""
    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 400
    
    data = request.get_json()
    if not data or not isinstance(data, dict):
        return jsonify({'error': 'Request body must be a JSON object'}), 400
    
    query = data.get('query', '')
    context = data.get('context', {})
    
    response = chatbot.process_query(query, context, blockchain, wallet_manager)
    
    return jsonify({'response': response})

@app.route('/api/blockchain', methods=['GET'])
def get_blockchain():
    """Get the entire blockchain"""
    return jsonify({
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
        'is_valid': blockchain.is_chain_valid()
    })

@app.route('/api/wallets', methods=['GET'])
def get_wallets():
    """Get all wallets"""
    return jsonify({
        'admin_wallets': wallet_manager.get_admin_wallets(),
        'student_wallets': wallet_manager.get_student_wallets()
    })

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get platform statistics"""
    all_skills = skill_extractor.get_all_skills()
    
    return jsonify({
        'total_certificates': len(blockchain.chain) - 1,
        'total_students': len(wallet_manager.get_student_wallets()),
        'total_admins': len(wallet_manager.get_admin_wallets()),
        'blockchain_length': len(blockchain.chain),
        'blockchain_valid': blockchain.is_chain_valid(),
        'total_skills': len(all_skills),
        'top_skills': all_skills[:10] if len(all_skills) > 10 else all_skills
    })

if __name__ == '__main__':
    # Initialize with genesis block if needed
    if len(blockchain.chain) == 0:
        blockchain.create_genesis_block()
    
    # Run the app
    app.run(host='0.0.0.0', port=5000, debug=True)
