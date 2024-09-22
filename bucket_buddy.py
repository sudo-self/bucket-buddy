import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QFileDialog, QListWidget, QMessageBox, QHBoxLayout, QSpacerItem, QSizePolicy,
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDesktopServices

class BucketBuddy(QWidget):
    def __init__(self):
        super().__init__()

        self.api_url = 'https://YOUR-DOMAIN.workers.dev'  <-- UPDATE THIS LINE
        self.init_ui()
        self.file_path = None

    def init_ui(self):
        layout = QVBoxLayout()
        self.setWindowTitle('Bucket🪣Buddy')

        self.header = QLabel('<a href="https://x.com/ilostmyipad" style="text-decoration: none; color: white;">@iLostMyipad</a>')
        self.header.setAlignment(Qt.AlignCenter)
        self.header.mousePressEvent = self.open_link
        layout.addWidget(self.header)

        self.key_input = QLineEdit(self)
        self.key_input.setPlaceholderText("🔑 Object key")
        layout.addWidget(self.key_input)

        self.file_input = QPushButton("Choose File", self)
        self.file_input.clicked.connect(self.choose_file)
        self.set_button_style(self.file_input, hover_color="#674876")
        layout.addWidget(self.file_input)

        button_layout = QHBoxLayout()

        self.put_button = QPushButton("PUT", self)
        self.put_button.clicked.connect(self.perform_put)
        self.set_button_style(self.put_button, hover_color="blue")
        button_layout.addWidget(self.put_button)

        self.get_button = QPushButton("GET", self)
        self.get_button.clicked.connect(self.perform_get)
        self.set_button_style(self.get_button, hover_color="green")
        button_layout.addWidget(self.get_button)

        self.delete_button = QPushButton("DELETE", self)
        self.delete_button.clicked.connect(self.perform_delete)
        self.set_button_style(self.delete_button, hover_color="#800000")
        button_layout.addWidget(self.delete_button)

        self.list_button = QPushButton("LIST", self)
        self.list_button.clicked.connect(self.list_objects)
        self.set_button_style(self.list_button, hover_color="black")
        button_layout.addWidget(self.list_button)

        layout.addLayout(button_layout)

        h_layout = QHBoxLayout()

        self.file_list = QListWidget(self)
        self.file_list.itemClicked.connect(self.item_clicked)
        h_layout.addWidget(self.file_list)

        self.image_preview = QLabel(self)
        self.image_preview.setAlignment(Qt.AlignCenter)
        self.image_preview.setFixedSize(400, 400)
        h_layout.addWidget(self.image_preview)

        layout.addLayout(h_layout)

        bottom_button_layout = QHBoxLayout()

        self.deploy_button = QPushButton("Deploy Worker", self)
        self.deploy_button.setStyleSheet("""
            QPushButton {
                border: 2px solid black;
                border-radius: 5px;
                background-color: transparent;
                color: white;
                padding: 8px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #ff9832;
                color: #000000;
            }
        """)
        self.deploy_button.clicked.connect(self.open_deploy_url)
        bottom_button_layout.addWidget(self.deploy_button)

        bottom_button_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.download_button = QPushButton("Download", self)
        self.download_button.clicked.connect(self.download_file)
        self.set_button_style(self.download_button, hover_color="#5555ff")
        bottom_button_layout.addWidget(self.download_button)

        layout.addLayout(bottom_button_layout)

        self.setLayout(layout)

    def set_button_style(self, button, hover_color="rgba(255, 255, 255, 0.2)"):
        button.setStyleSheet(f"""
            QPushButton {{
                border: 2px solid black;
                border-radius: 5px;
                background-color: transparent;
                color: white;
                padding: 8px;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
        """)

    def choose_file(self):
        options = QFileDialog.Options()
        self.file_path, _ = QFileDialog.getOpenFileName(self, "Add Object", "", "All Files (*)", options=options)
        if self.file_path:
            self.file_input.setText(self.file_path.split('/')[-1])

    def display_message(self, message, title="Info"):
        QMessageBox.information(self, title, message)

    def perform_put(self):
        key = self.key_input.text()
        if not key or not self.file_path:
            self.display_message('🔑 and 🗄 required', "Error")
            return
        
        try:
            with open(self.file_path, 'rb') as f:
                response = requests.put(f"{self.api_url}/{key}", files={'file': f})
            if response.ok:
                self.display_message(f"🤜✨🤛 {key} 🪣")
            else:
                self.display_message(f"Error: {response.text}", "Error")
        except Exception as e:
            self.display_message(f"Error: {str(e)}", "Error")

    def perform_get(self):
        key = self.key_input.text()
        if not key:
            self.display_message('🔑 required', "Error")
            return

        try:
            response = requests.get(f"{self.api_url}/{key}")
            if response.ok:
                with open("temp_image.jpg", 'wb') as img_file:
                    img_file.write(response.content)
                self.display_message(f"Fetched {key} successfully!")
            else:
                self.display_message(f"Error: {response.text}", "Error")
        except Exception as e:
            self.display_message(f"Error: {str(e)}", "Error")

    def perform_delete(self):
        key = self.key_input.text()
        if not key:
            self.display_message('🔑 required', "Error")
            return

        try:
            response = requests.delete(f"{self.api_url}/{key}")
            if response.ok:
                self.display_message(f"Object {key} Removed!")
            else:
                self.display_message(f"Error: {response.text}", "Error")
        except Exception as e:
            self.display_message(f"Error: {str(e)}", "Error")

    def list_objects(self):
        try:
            response = requests.get(f"{self.api_url}/list")
            data = response.json()
            if 'files' in data:
                self.file_list.clear()
                for file in data['files']:
                    self.file_list.addItem(file['key'])
            else:
                self.display_message('Unexpected response format: expected an array', "Error")
        except Exception as e:
            self.display_message(f"Error: {str(e)}", "Error")

    def item_clicked(self, item):
        self.key_input.setText(item.text())
        self.view_image(item)

    def view_image(self, item):
        key = item.text()
        response = requests.get(f"{self.api_url}/{key}")
        if response.ok:
            img_data = response.content
            pixmap = QPixmap()
            pixmap.loadFromData(img_data)

            self.image_preview.setPixmap(pixmap.scaled(self.image_preview.size(), aspectRatioMode=True))
            self.image_preview.setWindowTitle(key)
        else:
            self.display_message(f"Error: {response.text}", "Error")

    def download_file(self):
        key = self.key_input.text()
        if not key:
            self.display_message('🔑 required to download', "Error")
            return

        try:
            response = requests.get(f"{self.api_url}/{key}")
            if response.ok:
                file_path, _ = QFileDialog.getSaveFileName(self, "Save File", key, "All Files (*)")
                if file_path:
                    with open(file_path, 'wb') as file:
                        file.write(response.content)
                    self.display_message(f"Downloaded {key} successfully!")
            else:
                self.display_message(f"Error: {response.text}", "Error")
        except Exception as e:
            self.display_message(f"Error: {str(e)}", "Error")

    def open_deploy_url(self):
        url = QUrl("https://deploy.workers.cloudflare.com/?url=https://github.com/sudo-self/bucket-buddy")
        QDesktopServices.openUrl(url)

    def open_link(self, event):
        webbrowser.open("https://x.com/ilostmyipad")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    bucket_buddy = BucketBuddy()
    bucket_buddy.show()
    sys.exit(app.exec_())




