import sys, os
from tkinter import messagebox
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QLineEdit, QFileDialog, QVBoxLayout, QHBoxLayout
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from Crypto_Score import encrypt_file, decrypt_file, encrypt_folder, decrypt_folder
from Hash import calculate_hash
from Password import check_password_strength
from logger import log_event

original_hash = None

class AegisCrypt(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AegisCrypt")
        self.setFixedSize(520, 420)
        self.setStyleSheet("background-color:#0f172a; color:white;")

        title = QLabel("🛡 AegisCrypt")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.path = QLineEdit()
        self.path.setPlaceholderText("Select file or folder")
        self.path.setStyleSheet("background:#020617; padding:8px;")

        browse_file = QPushButton("File")
        browse_folder = QPushButton("Folder")

        browse_file.clicked.connect(self.pick_file)
        browse_folder.clicked.connect(self.pick_folder)

        pwd = QLabel("Password")
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.textChanged.connect(self.update_strength)

        self.strength = QLabel("Strength: ")
        self.hash_box = QLabel("SHA-256 Hash")
        self.hash_box.setWordWrap(True)

        enc = QPushButton("Encrypt")
        dec = QPushButton("Decrypt")
        enc.clicked.connect(self.encrypt)
        dec.clicked.connect(self.decrypt)

        for b in [browse_file, browse_folder, enc, dec]:
            b.setStyleSheet("background:#22d3ee; color:black; padding:8px;")

        row = QHBoxLayout()
        row.addWidget(browse_file)
        row.addWidget(browse_folder)

        buttons = QHBoxLayout()
        buttons.addWidget(enc)
        buttons.addWidget(dec)

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(self.path)
        layout.addLayout(row)
        layout.addWidget(pwd)
        layout.addWidget(self.password)
        layout.addWidget(self.strength)
        layout.addWidget(self.hash_box)
        layout.addLayout(buttons)

        self.setLayout(layout)

    def pick_file(self):
        self.path.setText(QFileDialog.getOpenFileName()[0])

    def pick_folder(self):
        self.path.setText(QFileDialog.getExistingDirectory())

    def update_strength(self):
        s, c = check_password_strength(self.password.text())
        self.strength.setText(f"Strength: {s}")
        self.strength.setStyleSheet(f"color:{c};")

    def encrypt(self):
        global original_hash
        p = self.path.text()
        pwd = self.password.text()
        if os.path.isdir(p):
            encrypt_folder(p, pwd)
        else:
            original_hash = calculate_hash(p)
            encrypt_file(p, pwd)
            self.hash_box.setText(f"SHA-256:\n{original_hash}")
        log_event(f"ENCRYPTED: {p}")

    def decrypt(self):
        p = self.path.text()
        pwd = self.password.text()
        if os.path.isdir(p):
            messagebox.showerror("Error", "Cannot decrypt folder path directly. Select the encrypted .zip.enc file.")
            return

        if p.endswith(".zip.enc"):
            out = decrypt_folder(p, pwd)
            self.hash_box.setText(f"Folder decrypted: {out}")
        elif p.endswith(".enc"):
            out = decrypt_file(p, pwd)
            new_hash = calculate_hash(out)
            status = "✔ VERIFIED" if new_hash == original_hash else "✖ MODIFIED"
            self.hash_box.setText(f"{new_hash}\n{status}")
        else:
            messagebox.showerror("Error", "Invalid encrypted file selected")

app = QApplication(sys.argv)
window = AegisCrypt()
window.show()
sys.exit(app.exec())
