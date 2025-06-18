import json
import sys
import requests
from datetime import datetime
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QListView, QMessageBox
)
from PySide6.QtCore import QStringListModel
import os

os.environ['NO_PROXY'] = '127.0.0.1'
SERVER_URL = "http://127.0.0.1:8000"


class ClientApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Клиент PySide6")
        self.resize(400, 300)
        
        self.click_count = 0
        
        # Элементы интерфейса
        self.input = QLineEdit(self)
        self.send_button = QPushButton("Отправить", self)
        self.load_button = QPushButton("Загрузить", self)
        self.list_view = QListView(self)
        self.model = QStringListModel()
        self.list_view.setModel(self.model)
        
        # Разметка
        layout = QVBoxLayout(self)
        layout.addWidget(self.input)
        layout.addWidget(self.send_button)
        layout.addWidget(self.load_button)
        layout.addWidget(self.list_view)
        
        # Сигналы
        self.send_button.clicked.connect(self.send_data)
        self.load_button.clicked.connect(self.load_data)
        
    def send_data(self):
        """Считывает текст из поля, собирает дату/время/номер клика и отправляет POST-запрос на сервер.
        В случае успеха — показывает сообщение об успехе, иначе — ошибку."""

        self.click_count += 1
        text = self.input.text()
        if not text:
            QMessageBox.warning(self, "Ошибка", "Поле ввода не может быть пустым")
            return

        now = datetime.now()
        payload = {
            "text": text,
            "date": now.strftime("%Y-%m-%d"),
            "time": now.strftime("%H:%M:%S"),
            "click_number": self.click_count
        }
        
        try:
            response = requests.post(f"{SERVER_URL}/submit", json=payload)
            response.raise_for_status()
            QMessageBox.information(self, "Успех", "Данные успешно отправлены")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при отправке: {e}")
    
    def load_data(self):
        """Отправляет GET-запрос на сервер для загрузки списка записей.
        Отображает полученные записи в QListView или сообщение об ошибке."""

        try:
            response = requests.get(f"{SERVER_URL}/records")
            response.raise_for_status()
            records = response.json()
            texts = [f"{r['date']} {r['time']} - {r['text']} (#{r['click_number']})" for r in records]
            self.model.setStringList(texts)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при получении: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ClientApp()
    window.show()
    sys.exit(app.exec())