import os
from utils import calculate_file_hash

class FileScanner:
    def __init__(self, api_client):
        self.api_client = api_client
        self.supported_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'}

    def scan(self, path, recursive=False):
        """Scan a file or directory for matches"""
        results = []

        if os.path.isfile(path):
            result = self._scan_file(path)
            if result:
                results.append(result)
        elif os.path.isdir(path):
            results.extend(self._scan_directory(path, recursive))

        return results

    def _scan_directory(self, directory, recursive):
        """Scan a directory for matching files"""
        results = []

        for entry in os.scandir(directory):
            if entry.is_file():
                result = self._scan_file(entry.path)
                if result:
                    results.append(result)
            elif entry.is_dir() and recursive:
                results.extend(self._scan_directory(entry.path, recursive))

        return results

    def _scan_file(self, file_path):
        """Scan a single file"""
        # Check if file extension is supported
        _, ext = os.path.splitext(file_path)
        if ext.lower() not in self.supported_extensions:
            print(f"Skipping unsupported file type: {file_path}")
            return None

        try:
            # Send the image directly to the API
            api_result = self.api_client.check_image(file_path)
            print(f"API Response for {file_path}: {api_result}")

            return {
                'file': file_path,
                'match': api_result['match'],
                'details': api_result.get('details', None)
            }

        except Exception as e:
            print(f"Error scanning {file_path}: {str(e)}")
            return {
                'file': file_path,
                'match': False,
                'error': str(e)
            }