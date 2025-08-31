import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QFileDialog, QMessageBox, QTextEdit
)
from encrypt_ssh_key import main as encrypt_main
from decrypt_ssh_key import decrypt_file  # Supongamos que ya implementaste decrypt_file(seed, input, output)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SSH Encryptor BIP-39")
        self.setGeometry(300, 300, 600, 400)

        self.layout = QVBoxLayout()

        # Archivo
        self.label_file = QLabel("Archivo SSH:")
        self.entry_file = QLineEdit()
        self.btn_file = QPushButton("Seleccionar archivo")
        self.btn_file.clicked.connect(self.select_file)
        self.layout.addWidget(self.label_file)
        self.layout.addWidget(self.entry_file)
        self.layout.addWidget(self.btn_file)

        # Frase BIP-39 para descifrar
        self.label_seed = QLabel("Frase BIP-39 (para descifrar):")
        self.entry_seed = QTextEdit()
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
        if not file_path:
            QMessageBox.warning(self, "Error", "Selecciona un archivo SSH")
            return

        try:
            # Aquí llamamos al main de encrypt_ssh_key
            # Capturamos la salida para mostrar la frase BIP-39
            import io, contextlib
            f = io.StringIO()
            with contextlib.redirect_stdout(f):
                encrypt_main(["--input", file_path])
            output = f.getvalue()

            QMessageBox.information(self, "Encrypt Completado", output)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def run_decrypt(self):
        file_path = self.entry_file.text()
        seed_words = self.entry_seed.toPlainText().strip()
        if not file_path or not seed_words:
            QMessageBox.warning(self, "Error", "Selecciona archivo y escribe la frase BIP-39")
            return

        try:
            output_file = file_path.replace(".enc", ".dec")
            decrypt_file(seed_words, file_path, output_file)
            QMessageBox.information(self, "Decrypt Completado", f"Archivo descifrado: {output_file}")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
