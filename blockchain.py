"""
Blockchain Implementation
Simulated blockchain for storing tamper-proof certificate records
"""

import hashlib
import json
from datetime import datetime
import os

class Block:
    """
    Individual block in the blockchain
    
    Structure:
    - index: Position in the chain
    - timestamp: When the block was created
    - data: Certificate information
    - previous_hash: Hash of the previous block (creates the chain)
    - hash: Current block's hash
    """
    
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()
    
    def calculate_hash(self):
        """
        Calculate SHA-256 hash of the block
        This ensures tamper-proof records - any change invalidates the hash
        """
        block_string = json.dumps({
            'index': self.index,
            'timestamp': self.timestamp,
            'data': self.data,
            'previous_hash': self.previous_hash
        }, sort_keys=True)
        
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def to_dict(self):
        """Convert block to dictionary for JSON serialization"""
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'data': self.data,
            'previous_hash': self.previous_hash,
            'hash': self.hash
        }

class Blockchain:
    """
    Blockchain ledger system
    
    Features:
    - Stores certificates in immutable chain
    - Validates chain integrity
    - Persists to JSON file
    - Searchable by certificate ID or wallet address
    """
    
    def __init__(self, storage_file='data/blockchain.json'):
        self.storage_file = storage_file
        self.chain = []
        self.load_from_file()
        
        # Create genesis block if chain is empty
        if len(self.chain) == 0:
            self.create_genesis_block()
    
    def create_genesis_block(self):
        """
        Create the first block in the blockchain
        The genesis block has no previous hash
        """
        genesis_block = Block(0, datetime.now().isoformat(), {
            'message': 'EduChain AI+ Genesis Block',
            'created': datetime.now().isoformat()
        }, '0')
        
        self.chain.append(genesis_block.to_dict())
        self.save_to_file()
    
    def get_latest_block(self):
        """Get the most recent block in the chain"""
        return self.chain[-1] if self.chain else None
    
    def add_certificate(self, certificate_data):
        """
        Add a new certificate to the blockchain
        
        Args:
            certificate_data: Dictionary containing certificate information
        
        Returns:
            The newly created block
        """
        latest_block = self.get_latest_block()
        new_index = latest_block['index'] + 1 if latest_block else 0
        previous_hash = latest_block['hash'] if latest_block else '0'
        
        new_block = Block(
            index=new_index,
            timestamp=datetime.now().isoformat(),
            data=certificate_data,
            previous_hash=previous_hash
        )
        
        self.chain.append(new_block.to_dict())
        self.save_to_file()
        
        return new_block.to_dict()
    
    def is_chain_valid(self):
        """
        Verify blockchain integrity
        
        Checks:
        1. Each block's hash is correct
        2. Each block's previous_hash matches the previous block's hash
        
        This detects any tampering with certificate data
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Recalculate current block's hash
            temp_block = Block(
                current_block['index'],
                current_block['timestamp'],
                current_block['data'],
                current_block['previous_hash']
            )
            
            # Check if hash matches
            if current_block['hash'] != temp_block.hash:
                return False
            
            # Check if previous_hash is correct
            if current_block['previous_hash'] != previous_block['hash']:
                return False
        
        return True
    
    def get_certificate_by_id(self, certificate_id):
        """
        Find a certificate by its ID
        
        Args:
            certificate_id: The unique certificate identifier
        
        Returns:
            Certificate data or None if not found
        """
        for block in self.chain:
            if 'data' in block and isinstance(block['data'], dict):
                if block['data'].get('certificate_id') == certificate_id:
                    return {
                        'certificate': block['data'],
                        'block_hash': block['hash'],
                        'timestamp': block['timestamp'],
                        'block_index': block['index']
                    }
        return None
    
    def get_certificates_by_wallet(self, wallet_address):
        """
        Get all certificates for a specific student wallet
        
        Args:
            wallet_address: Student's wallet address
        
        Returns:
            List of certificates
        """
        certificates = []
        for block in self.chain:
            if 'data' in block and isinstance(block['data'], dict):
                if block['data'].get('student_wallet') == wallet_address:
                    certificates.append({
                        'certificate': block['data'],
                        'block_hash': block['hash'],
                        'timestamp': block['timestamp']
                    })
        return certificates
    
    def save_to_file(self):
        """Persist blockchain to JSON file"""
        os.makedirs(os.path.dirname(self.storage_file), exist_ok=True)
        with open(self.storage_file, 'w') as f:
            json.dump(self.chain, f, indent=2)
    
    def load_from_file(self):
        """Load blockchain from JSON file"""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r') as f:
                    self.chain = json.load(f)
            except:
                self.chain = []

# UPGRADE NOTES FOR REAL BLOCKCHAIN:
# To upgrade to Polygon or Ethereum testnet:
# 1. Install web3.py: pip install web3
# 2. Connect to testnet: web3 = Web3(Web3.HTTPProvider('https://rpc-mumbai.maticvigil.com/'))
# 3. Deploy smart contract for certificate storage
# 4. Replace add_certificate() to call smart contract method
# 5. Use wallet private keys for transaction signing
# 6. Store IPFS hashes instead of full data on-chain
