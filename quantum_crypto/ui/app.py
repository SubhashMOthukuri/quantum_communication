"""
Quantum Secure Messenger - Flask Application

This module implements the main Flask application for the Quantum Secure Messenger.
It handles all web routes, quantum key exchange, message encryption/decryption,
and eavesdropper detection.

Classes:
    None

Functions:
    generate_quantum_key(): Generates a quantum key using BB84 protocol
    encrypt_message(message, key): Encrypts a message using quantum key
    decrypt_message(encrypted, key): Decrypts a message using quantum key
    detect_eve(measured_bases, received_bases): Detects eavesdropping attempts
    calculate_error_rate(measured_bases, received_bases): Calculates error rate
    add_message_to_chat(message, is_sent, user): Adds message to chat history
    update_chat_size(): Updates chat container size
    scroll_to_bottom(): Scrolls chat to bottom
    handle_file_upload(): Handles file uploads
    handle_typing(): Handles typing indicators
    handle_message(): Handles message sending/receiving

Routes:
    /: Landing page
    /chat: Chat interface
    /exchange_key: Quantum key exchange
    /upload: File upload
    /typing: Typing indicator
    /message: Message handling

Dependencies:
    - Flask
    - Qiskit
    - NumPy
    - Cryptography
"""

from flask import Flask, render_template, request, jsonify, send_file
import numpy as np
from cryptography.fernet import Fernet
import os
import json
from datetime import datetime
import logging
from typing import Dict, Any, Optional, Tuple
import random
import socketio
import eventlet
import base64

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__, 
    template_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '../templates')),
    static_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), 'static'))
)

# Initialize Socket.IO
sio = socketio.Server(cors_allowed_origins='*')
wsgi_app = socketio.WSGIApp(sio, app)

# Configure folders
UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '../uploads'))
ENCRYPTED_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '../encrypted_files'))
DECRYPTED_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '../decrypted_files'))

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(ENCRYPTED_FOLDER, exist_ok=True)
os.makedirs(DECRYPTED_FOLDER, exist_ok=True)

# Global variables for chat history and quantum state
chat_history = {
    'subhash': [],
    'ram': []
}
quantum_state = {
    'key_alice': None,
    'key_bob': None,
    'error_rate': 0.0,
    'eve_detected': False
}

def measure_qubit(qubit_state, measurement_basis):
    """Simulate quantum measurement"""
    if measurement_basis == qubit_state[1]:  # Same basis
        return qubit_state[0]
    else:  # Different basis
        return random.randint(0, 1)

def bb84_protocol(num_bits=10, eve_present=False):
    """
    Simulate BB84 protocol without Qiskit
    
    Args:
        num_bits (int): Number of bits to generate
        eve_present (bool): Whether Eve is present
        
    Returns:
        tuple: (alice_key, bob_key, eve_detected)
    """
    # Alice's random bits and bases
    alice_bits = [random.randint(0, 1) for _ in range(num_bits)]
    alice_bases = [random.randint(0, 1) for _ in range(num_bits)]
    
    # Create qubits (bit, basis)
    qubits = list(zip(alice_bits, alice_bases))
    
    # Eve's intervention
    if eve_present:
        eve_bases = [random.randint(0, 1) for _ in range(num_bits)]
        # Eve measures and resends
        for i in range(num_bits):
            measured_bit = measure_qubit(qubits[i], eve_bases[i])
            qubits[i] = (measured_bit, eve_bases[i])
    
    # Bob's random bases
    bob_bases = [random.randint(0, 1) for _ in range(num_bits)]
    
    # Bob's measurements
    bob_bits = [measure_qubit(qubits[i], bob_bases[i]) for i in range(num_bits)]
    
    # Keep only bits where bases match
    key_alice, key_bob = [], []
    for i in range(num_bits):
        if alice_bases[i] == bob_bases[i]:
            key_alice.append(alice_bits[i])
            key_bob.append(bob_bits[i])
    
    # Test for Eve's presence
    if len(key_alice) > 0:
        test_bits = random.sample(range(len(key_alice)), min(3, len(key_alice)))
        errors = sum(1 for i in test_bits if key_alice[i] != key_bob[i])
        error_rate = errors / len(test_bits) if test_bits else 0
        eve_detected = error_rate > 0.25
    else:
        eve_detected = True
    
    return key_alice, key_bob, eve_detected

# Generate encryption key
def generate_key(shared_bits):
    key_str = ''.join(str(bit) for bit in shared_bits)
    key_bytes = key_str.encode('utf-8')
    key = base64.urlsafe_b64encode(key_bytes.ljust(32)[:32])
    return Fernet(key)

# Encrypt message
def encrypt_message(message, key):
    return key.encrypt(message.encode()).decode()

# Decrypt message
def decrypt_message(encrypted_message, key):
    return key.decrypt(encrypted_message.encode()).decode()

def detect_eve(measured_bases: str, received_bases: str) -> bool:
    """
    Detects potential eavesdropping attempts by analyzing error rates.
    
    Args:
        measured_bases (str): The bases used for measurement
        received_bases (str): The bases received from the other party
    
    Returns:
        bool: True if eavesdropping is detected, False otherwise
    """
    try:
        error_rate = calculate_error_rate(measured_bases, received_bases)
        return error_rate > 0.25  # Threshold for Eve detection
    except Exception as e:
        logger.error(f"Error detecting Eve: {str(e)}")
        return True  # Assume Eve is present if detection fails

def calculate_error_rate(measured_bases: str, received_bases: str) -> float:
    """
    Calculates the error rate between measured and received bases.
    
    Args:
        measured_bases (str): The bases used for measurement
        received_bases (str): The bases received from the other party
    
    Returns:
        float: The calculated error rate
    """
    try:
        if len(measured_bases) != len(received_bases):
            return 1.0
        
        errors = sum(1 for m, r in zip(measured_bases, received_bases) if m != r)
        return errors / len(measured_bases)
    except Exception as e:
        logger.error(f"Error calculating error rate: {str(e)}")
        return 1.0

def add_message_to_chat(message: str, is_sent: bool, user: str) -> None:
    """
    Adds a message to the chat history.
    
    Args:
        message (str): The message to add
        is_sent (bool): Whether the message was sent by the user
        user (str): The user identifier ('subhash' or 'ram')
    """
    try:
        timestamp = datetime.now().strftime("%H:%M:%S")
        chat_history[user].append({
            'message': message,
            'is_sent': is_sent,
            'timestamp': timestamp
        })
        logger.info(f"Added message to chat for user {user}")
    except Exception as e:
        logger.error(f"Error adding message to chat: {str(e)}")

def update_chat_size() -> None:
    """
    Updates the chat container size based on content.
    This function is called via JavaScript to maintain proper scrolling.
    """
    try:
        # This function is implemented in JavaScript
        pass
    except Exception as e:
        logger.error(f"Error updating chat size: {str(e)}")

def scroll_to_bottom() -> None:
    """
    Scrolls the chat container to the bottom.
    This function is called via JavaScript to show latest messages.
    """
    try:
        # This function is implemented in JavaScript
        pass
    except Exception as e:
        logger.error(f"Error scrolling to bottom: {str(e)}")

def handle_file_upload(file: Any, user: str) -> Dict[str, Any]:
    """
    Handles file uploads in the chat.
    
    Args:
        file: The uploaded file
        user (str): The user identifier ('subhash' or 'ram')
    
    Returns:
        Dict[str, Any]: Response containing file details and status
    """
    try:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            return {
                'success': True,
                'filename': filename,
                'size': os.path.getsize(file_path)
            }
        return {'success': False, 'error': 'Invalid file type'}
    except Exception as e:
        logger.error(f"Error handling file upload: {str(e)}")
        return {'success': False, 'error': str(e)}

def handle_typing(user: str) -> Dict[str, Any]:
    """
    Handles typing indicators in the chat.
    
    Args:
        user (str): The user identifier ('subhash' or 'ram')
    
    Returns:
        Dict[str, Any]: Response containing typing status
    """
    try:
        return {'success': True, 'user': user}
    except Exception as e:
        logger.error(f"Error handling typing indicator: {str(e)}")
        return {'success': False, 'error': str(e)}

# Socket.IO event handlers
@sio.event
def connect(sid, environ):
    print(f"Client connected: {sid}")

@sio.event
def disconnect(sid):
    print(f"Client disconnected: {sid}")

@sio.event
def message(sid, data):
    print(f"Received message from {sid}: {data}")
    sio.emit('message', data)

@sio.event
def eve_enabled(sid, data):
    print(f"Eve detection {data['enabled']} for {data['sender']}")
    sio.emit('eve_status', data)

@app.route('/message', methods=['POST'])
def handle_message():
    data = request.get_json()
    message = data.get('message')
    sender = data.get('sender')
    eve_enabled = data.get('eve_enabled', False)
    
    if not message or not sender:
        return jsonify({'error': 'Missing message or sender'}), 400

    # Generate quantum key if not exists
    if 'quantum_key' not in quantum_state:
        quantum_state['quantum_key'] = generate_quantum_key()
    
    # Encrypt message
    encrypted_message = encrypt_message(message, quantum_state['quantum_key'])
    
    # Simulate Eve's interference if enabled
    if eve_enabled:
        # Simulate 30% chance of interference
        if random.random() < 0.3:
            # Modify the encrypted message to simulate interference
            modified_message = ''.join('1' if c == '0' else '0' for c in encrypted_message)
            encrypted_message = modified_message
            quantum_state['eve_detected'] = True
        else:
            quantum_state['eve_detected'] = False
    else:
        quantum_state['eve_detected'] = False

    # Decrypt message (simulating transmission)
    decrypted_message = decrypt_message(encrypted_message, quantum_state['quantum_key'])
    
    # Calculate error rate
    error_rate = calculate_error_rate(quantum_state['quantum_key'], encrypted_message)
    
    # Add messages to chat history
    chat_history[sender].append({
        'sender': sender,
        'message': message,
        'encrypted': encrypted_message,
        'decrypted': decrypted_message,
        'key': quantum_state['quantum_key'],
        'error_rate': error_rate,
        'eve_detected': quantum_state['eve_detected']
    })
    
    # Emit message to both users
    sio.emit('message', {
        'sender': sender,
        'message': decrypted_message,
        'encryption_details': {
            'key': quantum_state['quantum_key'],
            'encrypted': encrypted_message,
            'error_rate': error_rate
        },
        'eve_detected': quantum_state['eve_detected']
    })
    
    return jsonify({
        'success': True,
        'message': decrypted_message,
        'encrypted': encrypted_message,
        'key': quantum_state['quantum_key'],
        'error_rate': error_rate,
        'eve_detected': quantum_state['eve_detected']
    })

# Route handlers with docstrings
@app.route('/')
def index():
    """
    Renders the landing page.
    
    Returns:
        str: Rendered landing page template
    """
    return render_template('landing.html')

@app.route('/chat')
def chat():
    """
    Renders the chat interface.
    
    Returns:
        str: Rendered chat interface template
    """
    return render_template('index.html')

@app.route('/exchange_key', methods=['POST'])
def exchange_key():
    """
    Handles quantum key exchange between users.
    
    Returns:
        Dict[str, Any]: Response containing key exchange status and details
    """
    try:
        data = request.get_json()
        message = data.get('message')
        eve_enabled = data.get('eve_enabled')
        
        # Generate quantum key
        key_alice, key_bob, error_rate = bb84_protocol(num_bits=10, eve_present=eve_enabled)
        
        # Encrypt message
        encrypted = encrypt_message(message, generate_key(key_alice))
        
        # Check for Eve
        eve_detected = detect_eve(key_alice, key_bob)  # Simplified for demo
        
        return jsonify({
            'success': not eve_detected,
            'key': ''.join(str(bit) for bit in key_alice),
            'encrypted': encrypted,
            'error_rate': error_rate
        })
    except Exception as e:
        logger.error(f"Error in key exchange: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/upload', methods=['POST'])
def upload():
    """
    Handles file uploads in the chat.
    
    Returns:
        Dict[str, Any]: Response containing file upload status and details
    """
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file part'})
        
        file = request.files['file']
        user = request.form.get('user', 'subhash')
        
        result = handle_file_upload(file, user)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in file upload: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/typing', methods=['POST'])
def typing():
    """
    Handles typing indicators in the chat.
    
    Returns:
        Dict[str, Any]: Response containing typing status
    """
    try:
        data = request.get_json()
        user = data.get('user', 'subhash')
        
        result = handle_typing(user)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in typing indicator: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    # Create necessary folders
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(ENCRYPTED_FOLDER, exist_ok=True)
    os.makedirs(DECRYPTED_FOLDER, exist_ok=True)
    
    # Start the eventlet server
    eventlet.wsgi.server(eventlet.listen(('', 5000)), wsgi_app) 