'''
from typing import Any
import requests

class ScanService:
    def __init__(self, scan_api_url: str):
        self.scan_api_url = scan_api_url

    'def scan_file(self, file_path: str) -> dict[str, Any]:
        with open(file_path, 'rb') as file:
            response = requests.post(self.scan_api_url, files={'file': file})
            return response.json()
    def scan_file(file):
        # Mock scan: always return clean for local testing
        return {"is_clean": True}

    def is_file_safe(self, file_path: str) -> bool:
        scan_result = self.scan_file(file_path)
        return scan_result.get('is_safe', False)
'''
def scan_file(file):
    # Mock scan: always return clean for local testing
    return {"is_clean": True}