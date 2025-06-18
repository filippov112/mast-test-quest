import unittest
from unittest.mock import patch, MagicMock
from PySide6.QtWidgets import QApplication
import sys

from client.main import ClientApp

app = QApplication(sys.argv)

class TestClientApp(unittest.TestCase):
    def setUp(self):
        self.client_app = ClientApp()

    @patch("requests.post")
    def test_send_data_success(self, mock_post):
        """Проверяет отправку данных из GUI-клиента при заполненном поле. Проверяется:
        - увеличение click_count;
        - успешный вызов requests.post;
        - правильность формируемого JSON."""
    
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        self.client_app.input.setText("Тестовое сообщение")
        self.client_app.click_count = 0

        self.client_app.send_data()

        self.assertEqual(self.client_app.click_count, 1)
        mock_post.assert_called_once()

        args, kwargs = mock_post.call_args
        self.assertIn("json", kwargs)
        data = kwargs["json"]
        self.assertEqual(data["text"], "Тестовое сообщение")
        self.assertEqual(data["click_number"], 1)

    @patch("requests.post")
    def test_send_data_empty_text(self, mock_post):
        """Проверяет, что при пустом поле не происходит отправки и появляется предупреждение."""

        self.client_app.input.setText("")
        with patch("PySide6.QtWidgets.QMessageBox.warning") as mock_warning:
            self.client_app.send_data()
            mock_warning.assert_called_once()
        mock_post.assert_not_called()

    @patch("requests.get")
    def test_load_data_success(self, mock_get):
        """Проверяет загрузку записей с сервера и отображение в QListView.
        Мокирует GET-запрос, убеждается в корректности форматирования данных."""

        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = [
            {
                "date": "2025-06-17",
                "time": "12:34:56",
                "text": "Запись 1",
                "click_number": 5
            }
        ]
        mock_get.return_value = mock_response

        self.client_app.load_data()

        strings = self.client_app.model.stringList()
        self.assertEqual(len(strings), 1)
        self.assertIn("2025-06-17 12:34:56 - Запись 1 (#5)", strings[0])

    @patch("requests.get")
    def test_load_data_failure(self, mock_get):
        """Проверяет обработку ошибки при неудачном GET-запросе (например, ошибка сети).
        Убеждается, что вызывается QMessageBox с ошибкой."""

        mock_get.side_effect = Exception("Ошибка сети")

        with patch("PySide6.QtWidgets.QMessageBox.critical") as mock_critical:
            self.client_app.load_data()
            mock_critical.assert_called_once()

if __name__ == "__main__":
    unittest.main()