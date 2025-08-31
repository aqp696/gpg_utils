# app.py
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox
from encrypt_ssh_key import encrypt_file
from decrypt_ssh_key import decrypt_file

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SSH/GPG Encryptor")
        self.setGeometry(300, 300, 500, 200)

        self.layout = QVBoxLayout()

        # Archivo
        self.label_file = QLabel("Archivo:")
        self.entry_file = QLineEdit()
        self.btn_file = QPushButton("Seleccionar archivo")
        self.btn_file.clicked.connect(self.select_file)
        self.layout.addWidget(self.label_file)
        self.layout.addWidget(self.entry_file)
        self.layout.addWidget(self.btn_file)

        # Seed
        self.label_seed = QLabel("Seed:")
        self.entry_seed = QLineEdit()
        self.layout.addWidget(self.label_seed)
        self.layout.addWidget(self.entry_seed)

        # Botones
        self.btn_encrypt = QPushButton("Encrypt")
        self.btn_encrypt.clicked.connect(self.run_encrypt)
        self.btn_decrypt = QPushButton("Decrypt")
        self.btn_decrypt.clicked.connect(self.run_decrypt)
        self.layout.addWidget(self.btn_encrypt)
        self.layout.addWidget(self.btn_decrypt)

        self.setLayout(self.layout)

    def select_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo")
        if path:
            self.entry_file.setText(path)

    def run_encrypt(self):
        file_path = self.entry_file.text()
        seed = self.entry_seed.text()
        if not file_path or not seed:
            QMessageBox.warning(self, "Error", "Selecciona archivo y escribe la seed")
            return
        try:
            out_file = encrypt_file(file_path, seed)
            QMessageBox.information(self, "Éxito", f"Archivo cifrado: {out_file}")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def run_decrypt(self):
        file_path = self.entry_file.text()
        seed = self.entry_seed.text()
        if not file_path or not seed:
            QMessageBox.warning(self, "Error", "Selecciona archivo y escribe la seed")
            return
        try:
            out_file = decrypt_file(file_path, seed)
            QMessageBox.information(self, "Éxito", f"Archivo descifrado: {out_file}")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
