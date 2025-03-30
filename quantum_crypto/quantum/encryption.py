"""
Quantum Encryption Module

This module handles message encryption and decryption using quantum keys.
It implements quantum-resistant encryption algorithms and provides
secure message handling.

Classes:
    QuantumEncryption: Handles message encryption and decryption

Functions:
    encrypt_message(): Encrypts a message using quantum key
    decrypt_message(): Decrypts a message using quantum key
    validate_key(): Validates quantum key
    generate_iv(): Generates initialization vector

Dependencies:
    - Cryptography
    - NumPy
"""

from cryptography.fernet import Fernet
import numpy as np
from typing import Tuple, Optional
import logging
import base64
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class QuantumEncryption:
    """
    A class to handle quantum-based message encryption and decryption.
    
    Attributes:
        key (bytes): The quantum key for encryption/decryption
        fernet (Fernet): The Fernet encryption instance
        iv_length (int): Length of initialization vector
    
    Methods:
        encrypt(): Encrypts a message
        decrypt(): Decrypts a message
        validate_key(): Validates the quantum key
        generate_iv(): Generates initialization vector
    """
    
    def __init__(self, key: Optional[bytes] = None):
        """
        Initialize the QuantumEncryption.
        
        Args:
            key (Optional[bytes]): The quantum key to use
        """
        self.key = key or Fernet.generate_key()
        self.fernet = Fernet(self.key)
        self.iv_length = 16
    
    def encrypt(self, message: str) -> Tuple[str, bytes]:
        """
        Encrypts a message using the quantum key.
        
        Args:
            message (str): The message to encrypt
        
        Returns:
            Tuple[str, bytes]: A tuple containing:
                - The encrypted message as a string
                - The initialization vector used
        
        Raises:
            Exception: If encryption fails
        """
        try:
            # Generate initialization vector
            iv = self.generate_iv()
            
            # Convert message to bytes
            message_bytes = message.encode()
            
            # Pad message if necessary
            padded_message = self._pad_message(message_bytes)
            
            # Encrypt message
            encrypted = self.fernet.encrypt(padded_message)
            
            # Combine IV and encrypted message
            final_message = base64.b64encode(iv + encrypted).decode()
            
            return final_message, iv
        except Exception as e:
            logger.error(f"Error encrypting message: {str(e)}")
            raise
    
    def decrypt(self, encrypted_message: str) -> str:
        """
        Decrypts a message using the quantum key.
        
        Args:
            encrypted_message (str): The encrypted message to decrypt
        
        Returns:
            str: The decrypted message
        
        Raises:
            Exception: If decryption fails
        """
        try:
            # Decode the message
            message_bytes = base64.b64decode(encrypted_message)
            
            # Extract IV and encrypted data
            iv = message_bytes[:self.iv_length]
            encrypted = message_bytes[self.iv_length:]
            
            # Decrypt message
            decrypted = self.fernet.decrypt(encrypted)
            
            # Remove padding
            unpadded = self._unpad_message(decrypted)
            
            return unpadded.decode()
        except Exception as e:
            logger.error(f"Error decrypting message: {str(e)}")
            raise
    
    def validate_key(self) -> bool:
        """
        Validates the quantum key.
        
        Returns:
            bool: True if key is valid, False otherwise
        """
        try:
            # Check key length
            if len(self.key) != 32:
                return False
            
            # Check key format
            try:
                base64.b64decode(self.key)
                return True
            except:
                return False
        except Exception as e:
            logger.error(f"Error validating key: {str(e)}")
            return False
    
    def generate_iv(self) -> bytes:
        """
        Generates a random initialization vector.
        
        Returns:
            bytes: The generated initialization vector
        """
        try:
            return os.urandom(self.iv_length)
        except Exception as e:
            logger.error(f"Error generating IV: {str(e)}")
            raise
    
    def _pad_message(self, message: bytes) -> bytes:
        """
        Pads a message to the required length.
        
        Args:
            message (bytes): The message to pad
        
        Returns:
            bytes: The padded message
        """
        try:
            padding_length = 16 - (len(message) % 16)
            padding = bytes([padding_length] * padding_length)
            return message + padding
        except Exception as e:
            logger.error(f"Error padding message: {str(e)}")
            raise
    
    def _unpad_message(self, message: bytes) -> bytes:
        """
        Removes padding from a message.
        
        Args:
            message (bytes): The padded message
        
        Returns:
            bytes: The unpadded message
        """
        try:
            padding_length = message[-1]
            return message[:-padding_length]
        except Exception as e:
            logger.error(f"Error unpadding message: {str(e)}")
            raise

def encrypt_message(message: str, key: bytes) -> str:
    """
    Encrypts a message using a quantum key.
    
    Args:
        message (str): The message to encrypt
        key (bytes): The quantum key to use
    
    Returns:
        str: The encrypted message
    """
    try:
        encryption = QuantumEncryption(key)
        encrypted, _ = encryption.encrypt(message)
        return encrypted
    except Exception as e:
        logger.error(f"Error encrypting message: {str(e)}")
        raise

def decrypt_message(encrypted: str, key: bytes) -> str:
    """
    Decrypts a message using a quantum key.
    
    Args:
        encrypted (str): The encrypted message
        key (bytes): The quantum key to use
    
    Returns:
        str: The decrypted message
    """
    try:
        encryption = QuantumEncryption(key)
        return encryption.decrypt(encrypted)
    except Exception as e:
        logger.error(f"Error decrypting message: {str(e)}")
        raise

def validate_key(key: bytes) -> bool:
    """
    Validates a quantum key.
    
    Args:
        key (bytes): The key to validate
    
    Returns:
        bool: True if key is valid, False otherwise
    """
    try:
        encryption = QuantumEncryption(key)
        return encryption.validate_key()
    except Exception as e:
        logger.error(f"Error validating key: {str(e)}")
        return False

def generate_iv() -> bytes:
    """
    Generates a random initialization vector.
    
    Returns:
        bytes: The generated initialization vector
    """
    try:
        return os.urandom(16)
    except Exception as e:
        logger.error(f"Error generating IV: {str(e)}")
        raise 