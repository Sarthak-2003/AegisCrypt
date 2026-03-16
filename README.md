# AegisCrypt
AegisCrypt – Secure File Encryption Tool
It is a secure file encryption application built in Python that protects sensitive files and folders using modern cryptographic techniques. The application provides a user-friendly GUI and implements AES-256 encryption with password-derived keys to ensure strong data security. It is designed for students, developers, and professionals who want a simple but powerful tool to encrypt confidential documents and verify file integrity.
📌 Features
🔒 Secure Encryption

Uses AES-256 encryption (AES-GCM mode) for strong data protection.

Prevents unauthorized access to sensitive files.

🔑 Password-Based Key Derivation

Uses PBKDF2 with SHA-256 to generate secure encryption keys.

Protects against brute-force attacks.

📁 File and Folder Encryption

Encrypt individual files or entire folders.

Useful for protecting project files, documents, and backups.

🧮 File Integrity Verification

Generates SHA-256 hash to verify file integrity.

Detects any modification or tampering.

🔍 Password Strength Analyzer

Evaluates password security.

Encourages stronger passwords for better protection.

📝 Security Event Logging

Records encryption and decryption events.

Helps monitor security activities.

🖥 User-Friendly Interface

Built using PyQt6.

Simple interface designed for easy usage.

🏗 Project Architecture
AegisCrypt/
│
├── main.py                # Application entry point
├── encryption.py          # AES encryption & decryption logic
├── password_utils.py      # Password strength checker
├── hash_utils.py          # SHA-256 hashing functions
├── logger.py              # Security logging system
│
├── gui/
│   ├── main_window.py     # PyQt6 GUI layout
│   ├── encrypt_window.py  # Encryption interface
│   └── decrypt_window.py  # Decryption interface
│
├── logs/
│   └── security.log       # Activity logs
├── requirements.txt
└── README.md
