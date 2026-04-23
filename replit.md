# EduChain AI+ - Blockchain & AI-Powered Credential Verification Platform

## Overview
EduChain AI+ is a comprehensive full-stack web application that combines blockchain technology with artificial intelligence to create tamper-proof educational credentials, NFT achievement badges, and intelligent career matching.

## Project Purpose
- **Blockchain-backed certificates**: Immutable credential storage using simulated blockchain
- **NFT badges**: Unique digital badges for each certificate
- **AI skill extraction**: Automatic skill identification from course data
- **AI resume generation**: Professional PDF resumes from verified credentials
- **AI job matching**: Intelligent job recommendations based on skills
- **QR verification**: Quick certificate authentication via QR codes

## Technology Stack
### Backend
- **Python 3.11** - Core programming language
- **Flask** - Web framework
- **Flask-CORS** - Cross-origin resource sharing
- **Blockchain simulation** - Custom implementation with SHA-256 hashing
- **Wallet system** - Admin and student wallet management

### AI & ML
- **NLTK** - Natural language processing for skill extraction
- **scikit-learn** - Job matching algorithms (TF-IDF, cosine similarity)
- **Pillow** - NFT badge image generation
- **reportlab** - PDF resume generation
- **qrcode** - QR code generation

### Frontend
- **HTML5** - Structure
- **TailwindCSS** - Styling (via CDN)
- **Vanilla JavaScript** - Interactivity
- **Responsive design** - Mobile-friendly interface

## Project Architecture

### Core Modules
1. **blockchain.py** - Blockchain ledger system
   - Block creation with hash chains
   - Certificate storage
   - Chain validation
   - JSON persistence

2. **wallet.py** - Wallet management
   - Admin wallet creation
   - Student wallet creation
   - Balance tracking
   - Skill/NFT storage

3. **nft_generator.py** - NFT badge creation
   - Colorful certificate-specific designs
   - Pillow-based image generation
   - Metadata management

4. **ai_skills.py** - AI skill extraction
   - NLP-based keyword matching
   - Course-to-skill mapping
   - Skill database
   - Grade-based enhancements

5. **ai_resume.py** - Resume generation
   - PDF creation with reportlab
   - AI-generated summaries
   - Professional formatting
   - Blockchain verification badges

6. **ai_jobs.py** - Job matching
   - TF-IDF vectorization
   - Cosine similarity matching
   - Mock job database
   - Match percentage scoring

7. **ai_chatbot.py** - Chatbot assistant
   - Rule-based query processing
   - Certificate verification
   - Context-aware responses
   - Action suggestions

8. **qr_generator.py** - QR code creation
   - Verification URL encoding
   - High error correction
   - PNG output

### API Routes
- `/api/register_student` - Create student wallet
- `/api/create_admin_wallet` - Create admin wallet
- `/api/issue_certificate` - Issue new certificate with NFT
- `/api/verify_certificate/<id>` - Verify certificate authenticity
- `/api/student_certificates/<wallet>` - Get student's certificates
- `/api/generate_resume/<wallet>` - Generate AI resume
- `/api/recommend_jobs/<wallet>` - Get job recommendations
- `/api/chatbot_query` - Process chatbot queries
- `/api/blockchain` - View blockchain data
- `/api/wallets` - List all wallets
- `/api/stats` - Platform statistics

### Frontend Pages
- **index.html** - Home page with features and verification
- **admin.html** - Admin dashboard for certificate issuance
- **student.html** - Student dashboard with certificates, NFTs, resume, jobs
- **verify.html** - Public certificate verification page

## Certificate Types
1. **Certificate of Completion** - Blue theme
2. **Certificate of Achievement** - Green theme
3. **Certificate of Excellence** - Purple theme
4. **Certificate of Participation** - Orange theme

## Features Implemented
✅ Blockchain simulation with hash chains
✅ Dual wallet system (admin/student)
✅ Four certificate template types
✅ NFT badge generation with Pillow
✅ QR code generation for verification
✅ AI skill extraction from certificates
✅ AI-powered resume generation (PDF)
✅ AI job matching with mock dataset
✅ Rule-based chatbot assistant
✅ Modern TailwindCSS interface
✅ Admin dashboard
✅ Student dashboard
✅ Public verification page
✅ Responsive design

## Data Storage
All data is stored in JSON files in the `data/` directory:
- `blockchain.json` - Complete blockchain
- `wallets.json` - All admin and student wallets
- `skills.json` - Skill tracking data
- `jobs.json` - Mock job listings

## Recent Changes
- **2025-10-19**: Bug fixes and API improvements
  - Fixed QR code generation to use actual Replit domain instead of localhost (now works when scanned from any device)
  - Fixed certificate issuance to properly add NFT badges to student wallets
  - Fixed admin wallet statistics to correctly track certificate issuance counts
  - Added three-layer JSON validation to all POST endpoints (content-type, data presence, type checking)

- **2025-10-19**: Initial implementation complete
  - Created full blockchain system
  - Implemented wallet management
  - Built all AI features (skill extraction, resume, job matching, chatbot)
  - Created NFT badge generator
  - Built complete frontend with TailwindCSS
  - Set up Flask API routes
  - Added QR code verification
  - Configured workflow for port 5000

## How to Use

### As Admin
1. Visit `/admin`
2. Create admin wallet for your institution
3. Register students to create their wallets
4. Issue certificates by selecting type, student, and course
5. System automatically generates NFT badges and QR codes
6. View blockchain and student data

### As Student
1. Visit `/student/<your_wallet_address>`
2. View all your blockchain-verified certificates
3. Browse your NFT badge collection
4. Generate AI-powered resume (PDF download)
5. Get personalized job recommendations
6. Chat with AI assistant

### Public Verification
1. Visit `/verify/<certificate_id>` or scan QR code
2. View full certificate details
3. See blockchain hash and verification
4. Check trust score
5. View NFT badge and QR code

## Deployment
The application runs on port 5000 and is configured for Replit deployment:
- Workflow: `Server` running `python app.py`
- Host: 0.0.0.0 (allows external access)
- Debug mode enabled for development

## Future Enhancements
Planned for next phase:
- Integration with real blockchain (Polygon/Ethereum testnet)
- IPFS for decentralized NFT storage
- Advanced AI chatbot with OpenAI/Anthropic
- Analytics dashboard with charts
- LinkedIn/social media certificate sharing
- Multi-signature wallet support
- Email notifications
- Certificate templates customization

## Upgrade Path to Real Blockchain
Code includes inline comments for upgrading to production blockchain:
1. Install web3.py
2. Connect to Polygon Mumbai or Ethereum Goerli testnet
3. Deploy smart contract for certificate storage
4. Use IPFS for NFT metadata
5. Implement proper key management
6. Add transaction fees handling

## Notes
- This is a simulated blockchain - perfect for demonstrations and prototypes
- All wallets use simulated private keys (not production-ready)
- Balances are demo tokens for issuance tracking
- AI features use lightweight libraries (NLTK, scikit-learn)
- TailwindCSS loaded via CDN (switch to build process for production)
- QR codes link to local URLs (update for production domain)

## Support
Built with Python Flask, blockchain simulation, and AI-powered features for educational credential management.
