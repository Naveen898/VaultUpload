import unittest
from unittest.mock import patch
from backend.services.scan_service import scan_file

class TestScanService(unittest.TestCase):

    @patch('backend.services.scan_service.virus_scanner')
    def test_scan_file_success(self, mock_scanner):
        mock_scanner.scan.return_value = True  # Simulate a clean file
        result = scan_file('test_file.txt')
        self.assertTrue(result)
        mock_scanner.scan.assert_called_once_with('test_file.txt')

    @patch('backend.services.scan_service.virus_scanner')
    def test_scan_file_virus_detected(self, mock_scanner):
        mock_scanner.scan.return_value = False  # Simulate a virus detected
        result = scan_file('infected_file.txt')
        self.assertFalse(result)
        mock_scanner.scan.assert_called_once_with('infected_file.txt')

    @patch('backend.services.scan_service.virus_scanner')
    def test_scan_file_error(self, mock_scanner):
        mock_scanner.scan.side_effect = Exception("Scanner error")  # Simulate an error
        with self.assertRaises(Exception) as context:
            scan_file('error_file.txt')
        self.assertEqual(str(context.exception), "Scanner error")
        mock_scanner.scan.assert_called_once_with('error_file.txt')

if __name__ == '__main__':
    unittest.main()