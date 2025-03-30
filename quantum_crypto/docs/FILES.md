# Project Files Documentation

## Table of Contents

1. [UI Files](#ui-files)
2. [Template Files](#template-files)
3. [Quantum Files](#quantum-files)
4. [Utility Files](#utility-files)
5. [Configuration Files](#configuration-files)
6. [Documentation Files](#documentation-files)

## UI Files

### `quantum_crypto/ui/app.py`

Main Flask application file that handles all web routes and server-side logic.

**Key Components:**

```python
# Main Routes
@app.route('/')              # Landing page
@app.route('/chat')          # Chat interface
@app.route('/exchange_key')  # Quantum key exchange

# Key Functions
def generate_quantum_key()   # Generates quantum key using BB84 protocol
def encrypt_message()        # Encrypts message using quantum key
def detect_eve()            # Detects eavesdropping attempts
```

**Dependencies:**

- Flask
- Qiskit
- NumPy
- Cryptography

## Template Files

### `quantum_crypto/templates/index.html`

Main chat interface template with split-screen design.

**Key Components:**

```html
<!-- Main Structure -->
<div class="container">
  # Main container
  <div class="split-container">
    # Split screen container
    <div class="user-panel">
      # Individual user panels
      <div class="chat-messages">
        # Message display area
        <div class="message-box"># Message input area</div>
      </div>
    </div>
  </div>
</div>
```

**Features:**

- Real-time message updates
- File attachment support
- Typing indicators
- Scroll management
- Security status display

### `quantum_crypto/templates/landing.html`

Landing page template with quantum stats display.

**Key Components:**

```html
<!-- Main Structure -->
<div class="container">
  # Main container
  <div class="quantum-stats">
    # Stats display
    <div class="stat-card"># Individual stat cards</div>
  </div>
</div>
```

**Features:**

- Quantum key display
- Encryption status
- Security monitoring
- Real-time updates

## Quantum Files

### `quantum_crypto/quantum/key_generator.py`

Handles quantum key generation using BB84 protocol.

**Key Functions:**

```python
def generate_quantum_key():
    """Generates quantum key using BB84 protocol"""
    qc = QuantumCircuit(2, 2)
    qc.h(0)  # Apply Hadamard gate
    qc.cx(0, 1)  # Apply CNOT gate
    qc.measure([0, 1], [0, 1])
    return qc

def sift_key():
    """Performs key sifting process"""
    # Implementation details
```

### `quantum_crypto/quantum/encryption.py`

Handles message encryption and decryption.

**Key Functions:**

```python
def encrypt_message(message, key):
    """Encrypts message using quantum key"""
    # Implementation details

def decrypt_message(encrypted, key):
    """Decrypts message using quantum key"""
    # Implementation details
```

### `quantum_crypto/quantum/eve_detection.py`

Implements eavesdropper detection system.

**Key Functions:**

```python
def detect_eve(measured_bases, received_bases):
    """Detects eavesdropping attempts"""
    error_rate = calculate_error_rate(measured_bases, received_bases)
    return error_rate > 0.1

def calculate_error_rate():
    """Calculates error rate in quantum measurements"""
    # Implementation details
```

## Utility Files

### `quantum_crypto/utils/helpers.py`

Contains utility functions for the project.

**Key Functions:**

```python
def format_message():
    """Formats message for display"""
    # Implementation details

def validate_file():
    """Validates file uploads"""
    # Implementation details

def log_event():
    """Logs system events"""
    # Implementation details
```

## Configuration Files

### `requirements.txt`

Lists all project dependencies with specific versions.

**Categories:**

- Core Dependencies
- Web Dependencies
- Security Dependencies
- File Handling
- Testing
- Development
- Monitoring
- Documentation

### `.env`

Environment configuration file (not tracked in git).

**Key Variables:**

```
FLASK_ENV=development
SECRET_KEY=your_secret_key
DEBUG=True
```

## Documentation Files

### `README.md`

Project overview and setup instructions.

**Sections:**

- Project Description
- Features
- Installation
- Usage
- Contributing
- License

### `quantum_crypto/docs/TECHNICAL.md`

Technical implementation details.

**Sections:**

- Architecture Overview
- Quantum Implementation
- Security Protocol
- UI Components
- API Endpoints
- Real-time Features
- File Handling
- Error Handling

### `quantum_crypto/docs/FILES.md`

This file - documentation for all project files.

## File Dependencies

### Frontend Dependencies

```html
<!-- index.html -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/js/all.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>
```

### Backend Dependencies

```python
# app.py
from flask import Flask, render_template, request, jsonify
from qiskit import QuantumCircuit
import numpy as np
from cryptography.fernet import Fernet
```

## File Organization

### Directory Structure

```
quantum_crypto/
├── ui/                    # User interface components
├── templates/             # HTML templates
├── quantum/              # Quantum computing components
├── utils/                # Utility functions
├── docs/                 # Documentation
└── tests/                # Test files
```

### File Naming Conventions

- Python files: lowercase with underscores
- HTML files: lowercase with hyphens
- Documentation: PascalCase with .md extension

## File Security

### Security Measures

1. Input validation in all files
2. XSS prevention in templates
3. CSRF protection in forms
4. Secure file handling
5. Environment variable protection

### File Permissions

- Python files: 644
- HTML files: 644
- Configuration files: 600
- Documentation files: 644

## File Maintenance

### Best Practices

1. Regular code reviews
2. Version control
3. Documentation updates
4. Security audits
5. Performance optimization

### Update Procedures

1. Update code
2. Update tests
3. Update documentation
4. Review changes
5. Deploy updates

## File Testing

### Test Coverage

- Unit tests for Python files
- Integration tests for UI
- Security tests for all components
- Performance tests for critical paths

### Testing Tools

- pytest for Python
- Jest for JavaScript
- Selenium for UI
- Security scanners
