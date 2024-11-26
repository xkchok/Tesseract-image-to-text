import sys
import re
import pytesseract
from PIL import ImageGrab, Image
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QMessageBox, QTextEdit, QCheckBox

# Set up Tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class ImageToTextExtractor(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.original_text = ""

    def initUI(self):
        self.setWindowTitle('Image to Text Extractor')
        layout = QVBoxLayout()

        self.btn_paste = QPushButton('Paste Image', self)
        self.btn_paste.clicked.connect(self.paste_image)
        layout.addWidget(self.btn_paste)

        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        layout.addWidget(self.text_edit)

        self.checkbox = QCheckBox('Remove newline characters', self)
        self.checkbox.stateChanged.connect(self.process_text)
        layout.addWidget(self.checkbox)
        
        self.btn_copy = QPushButton('Copy Text', self)
        self.btn_copy.clicked.connect(self.copy_text)
        layout.addWidget(self.btn_copy)

        self.setLayout(layout)
        self.setGeometry(300, 300, 400, 300)

    def paste_image(self):
        try:
            img = ImageGrab.grabclipboard()
            if isinstance(img, Image.Image):
                self.extract_text(img)
                self.btn_copy.setText('Copy Text') 
            else:
                QMessageBox.critical(self, "Error", "No image found in clipboard.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def extract_text(self, img):
        try:
            text = pytesseract.image_to_string(img)
            self.original_text = text
            self.text_edit.setText(text)
            self.process_text()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            
    def process_text(self):
        text = self.text_edit.toPlainText()
        if self.checkbox.isChecked():
            text = re.sub(r'\s+', ' ', text) # Replace newlines and multiple spaces with a single space
        else:
            text = self.original_text
        self.text_edit.setText(text)

    def copy_text(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.text_edit.toPlainText())
        self.btn_copy.setText('Copy Text ✓')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageToTextExtractor()
    ex.show()
    sys.exit(app.exec_())