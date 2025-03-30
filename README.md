# Quantum Secure Messenger

A real-time quantum-secure messaging application that demonstrates quantum key distribution (QKD) and quantum encryption principles. This project implements a secure communication channel between two users (Subhash and Ram) with the ability to detect eavesdropping attempts.

## 🌟 Features

- **Real-time Quantum Communication**: Secure messaging between two users using quantum encryption
- **Eve Detection**: Built-in eavesdropper detection system
- **Modern UI**: Beautiful, responsive interface with real-time updates
- **File Sharing**: Support for secure file transfers
- **Dark/Light Theme**: Customizable interface themes
- **Real-time Status Updates**: Live quantum key and encryption status monitoring
- **Message History**: Persistent chat history with encryption details
- **Typing Indicators**: Real-time typing status for both users
- **Scroll Management**: Smart scroll handling with bottom button
- **Responsive Design**: Works seamlessly on all device sizes

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Flask
- NumPy
- Qiskit (for quantum operations)

### Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/quantum-secure-messenger.git
cd quantum-secure-messenger
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the application:

```bash
cd quantum_crypto/ui
python app.py
```

4. Open your browser and navigate to:

```
http://127.0.0.1:5000
```

## 🛠️ Project Structure

```
quantum_crypto/
├── ui/
│   ├── app.py              # Flask application
│   └── static/             # Static assets
├── templates/
│   ├── index.html          # Main chat interface
│   └── landing.html        # Landing page
├── quantum/
│   ├── key_generator.py    # Quantum key generation
│   ├── encryption.py       # Message encryption/decryption
│   └── eve_detection.py    # Eavesdropper detection
└── utils/
    └── helpers.py          # Utility functions
```

## 🔒 Security Features

1. **Quantum Key Distribution (QKD)**

   - Uses quantum entanglement for key generation
   - Implements BB84 protocol
   - Real-time key refresh

2. **Eve Detection**

   - Continuous monitoring of quantum state
   - Error rate analysis
   - Visual security status indicators

3. **Message Encryption**
   - Quantum-resistant encryption
   - Real-time encryption status
   - Secure file transfer

## 💻 User Interface

### Main Features

1. **Chat Interface**

   - Split-screen design for both users
   - Real-time message updates
   - File attachment support
   - Typing indicators
   - Message status tracking

2. **Quantum Stats Panel**

   - Live quantum key display
   - Encryption status
   - Security monitoring
   - Eve detection status

3. **Message Features**
   - Text messages
   - File attachments
   - Encryption details
   - Timestamp tracking

## 🔧 Technical Details

### Quantum Implementation

- Uses Qiskit for quantum operations
- Implements BB84 protocol for key distribution
- Real-time quantum state monitoring
- Error rate calculation and analysis

### Security Measures

- Quantum-resistant encryption
- Continuous key refresh
- Eavesdropper detection
- Secure file transfer protocol

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Qiskit team for quantum computing framework
- Flask team for the web framework
- All contributors and users of the project

## 📞 Support

For support, email support@quantumsecuremessenger.com or join our Slack channel.

## 🔄 Updates

- Version 1.0.0: Initial release
- Version 1.1.0: Added file sharing
- Version 1.2.0: Enhanced UI/UX
- Version 1.3.0: Improved security features

## 📚 Documentation

For detailed documentation, visit our [Documentation Page](https://quantumsecuremessenger.com/docs).
