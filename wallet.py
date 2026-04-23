"""
Wallet Management System
Handles admin and student wallets for certificate issuance
"""

import hashlib
import json
import os
from datetime import datetime
import secrets

class WalletManager:
    """
    Manages admin and student wallets
    
    Wallet Types:
    1. Admin Wallet: Used by college authorities to issue certificates
    2. Student Wallet: Automatically created for students to receive certificates
    
    Each wallet has:
    - Wallet address (public key)
    - Private key (simulated)
    - Balance (demo tokens)
    - Associated metadata
    """
    
    def __init__(self, storage_file='data/wallets.json'):
        self.storage_file = storage_file
        self.wallets = {
            'admin': [],
            'student': []
        }
        self.load_from_file()
    
    def generate_wallet_address(self, wallet_type, identifier):
        """
        Generate a unique wallet address
        
        Format: WALLET_TYPE-HASH[:16]
        Example: ADMIN-a1b2c3d4e5f6g7h8 or STUDENT-x9y8z7w6v5u4t3s2
        """
        hash_input = f"{wallet_type}-{identifier}-{datetime.now().isoformat()}-{secrets.token_hex(8)}"
        hash_result = hashlib.sha256(hash_input.encode()).hexdigest()[:16]
        return f"{wallet_type.upper()}-{hash_result}"
    
    def generate_private_key(self):
        """
        Generate a simulated private key
        
        In production blockchain (Polygon/Ethereum):
        - Use secp256k1 elliptic curve cryptography
        - Private key is 256-bit random number
        - Never expose or log private keys
        """
        return secrets.token_hex(32)
    
    def create_admin_wallet(self, institution_name, admin_name):
        """
        Create an admin wallet for college authority
        
        Args:
            institution_name: Name of the college/institution
            admin_name: Name of the admin user
        
        Returns:
            Wallet data dictionary
        """
        wallet_address = self.generate_wallet_address('ADMIN', institution_name)
        private_key = self.generate_private_key()
        
        wallet = {
            'wallet_address': wallet_address,
            'private_key': private_key,
            'institution_name': institution_name,
            'admin_name': admin_name,
            'balance': 1000,  # Demo tokens for issuing certificates
            'created_at': datetime.now().isoformat(),
            'type': 'admin',
            'certificates_issued': 0
        }
        
        self.wallets['admin'].append(wallet)
        self.save_to_file()
        
        return wallet
    
    def create_student_wallet(self, name, email, student_id):
        """
        Create a student wallet
        
        Args:
            name: Student's full name
            email: Student's email
            student_id: Unique student identifier
        
        Returns:
            Wallet data dictionary
        """
        wallet_address = self.generate_wallet_address('STUDENT', student_id)
        private_key = self.generate_private_key()
        
        wallet = {
            'wallet_address': wallet_address,
            'private_key': private_key,
            'name': name,
            'email': email,
            'student_id': student_id,
            'balance': 0,  # Receives NFTs/certificates
            'created_at': datetime.now().isoformat(),
            'type': 'student',
            'certificates_received': 0,
            'skills': [],
            'nft_badges': []
        }
        
        self.wallets['student'].append(wallet)
        self.save_to_file()
        
        return wallet
    
    def get_admin_wallets(self):
        """Get all admin wallets"""
        # Return without private keys for security
        return [{
            'wallet_address': w['wallet_address'],
            'institution_name': w['institution_name'],
            'admin_name': w['admin_name'],
            'balance': w['balance'],
            'certificates_issued': w['certificates_issued']
        } for w in self.wallets['admin']]
    
    def get_student_wallets(self):
        """Get all student wallets"""
        # Return without private keys for security
        return [{
            'wallet_address': w['wallet_address'],
            'name': w['name'],
            'email': w['email'],
            'student_id': w['student_id'],
            'certificates_received': w['certificates_received'],
            'skills': w.get('skills', [])
        } for w in self.wallets['student']]
    
    def get_student_by_wallet(self, wallet_address):
        """Get student data by wallet address"""
        for wallet in self.wallets['student']:
            if wallet['wallet_address'] == wallet_address:
                # Return without private key
                return {
                    'wallet_address': wallet['wallet_address'],
                    'name': wallet['name'],
                    'email': wallet['email'],
                    'student_id': wallet['student_id'],
                    'skills': wallet.get('skills', []),
                    'nft_badges': wallet.get('nft_badges', []),
                    'certificates_received': wallet['certificates_received']
                }
        return None
    
    def add_skills_to_student(self, wallet_address, new_skills):
        """Add extracted skills to student profile"""
        for wallet in self.wallets['student']:
            if wallet['wallet_address'] == wallet_address:
                if 'skills' not in wallet:
                    wallet['skills'] = []
                # Add unique skills only
                for skill in new_skills:
                    if skill not in wallet['skills']:
                        wallet['skills'].append(skill)
                wallet['certificates_received'] = wallet.get('certificates_received', 0) + 1
                self.save_to_file()
                return True
        return False
    
    def add_nft_to_student(self, wallet_address, nft_data):
        """Add NFT badge to student wallet"""
        for wallet in self.wallets['student']:
            if wallet['wallet_address'] == wallet_address:
                if 'nft_badges' not in wallet:
                    wallet['nft_badges'] = []
                wallet['nft_badges'].append(nft_data)
                self.save_to_file()
                return True
        return False
    
    def increment_admin_issuance(self, wallet_address):
        """Increment certificate issuance count for admin"""
        for wallet in self.wallets['admin']:
            if wallet['wallet_address'] == wallet_address:
                wallet['certificates_issued'] = wallet.get('certificates_issued', 0) + 1
                self.save_to_file()
                return True
        return False
    
    def save_to_file(self):
        """Persist wallets to JSON file"""
        os.makedirs(os.path.dirname(self.storage_file), exist_ok=True)
        with open(self.storage_file, 'w') as f:
            json.dump(self.wallets, f, indent=2)
    
    def load_from_file(self):
        """Load wallets from JSON file"""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r') as f:
                    self.wallets = json.load(f)
            except:
                self.wallets = {'admin': [], 'student': []}

# WALLET INTERACTION NOTES:
# 1. Admin issues certificate → transaction recorded on blockchain
# 2. Student receives certificate → NFT badge added to wallet
# 3. Each transaction has sender (admin) and receiver (student) wallet IDs
# 4. Balance is demo only - in real blockchain, this would be actual cryptocurrency
# 5. Private keys should NEVER be exposed in production - stored encrypted
