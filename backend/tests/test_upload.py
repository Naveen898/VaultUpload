import unittest
from unittest.mock import patch, MagicMock
from backend.routes.upload_routes import upload_file
from backend.services.scan_service import scan_file
from backend.services.storage_service import store_file
from flask import Flask

class TestUploadRoutes(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.testing = True
        self.client = self.app.test_client()

    @patch('backend.services.scan_service.scan_file')
    @patch('backend.services.storage_service.store_file')
    def test_upload_file_success(self, mock_store_file, mock_scan_file):
        mock_scan_file.return_value = True  # Simulate a successful virus scan
        mock_store_file.return_value = 'file_url'  # Simulate successful file storage

        with self.app.test_request_context('/upload', method='POST', data={'file': (BytesIO(b'test file content'), 'test.txt')}):
            response = upload_file()

        self.assertEqual(response.status_code, 200)
        self.assertIn('file_url', response.get_json())

    @patch('backend.services.scan_service.scan_file')
    def test_upload_file_virus_detected(self, mock_scan_file):
        mock_scan_file.return_value = False  # Simulate a virus detected

        with self.app.test_request_context('/upload', method='POST', data={'file': (BytesIO(b'test file content'), 'test.txt')}):
            response = upload_file()

        self.assertEqual(response.status_code, 400)
        self.assertIn('Virus detected', response.get_json()['message'])

    @patch('backend.services.storage_service.store_file')
    def test_upload_file_storage_failure(self, mock_store_file):
        mock_store_file.side_effect = Exception("Storage error")  # Simulate storage failure

        with self.app.test_request_context('/upload', method='POST', data={'file': (BytesIO(b'test file content'), 'test.txt')}):
            response = upload_file()

        self.assertEqual(response.status_code, 500)
        self.assertIn('Storage error', response.get_json()['message'])

if __name__ == '__main__':
    unittest.main()