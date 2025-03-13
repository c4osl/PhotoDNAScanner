import requests
import mimetypes

class PhotoDNAClient:
    def __init__(self, api_key, api_endpoint=None):
        self.api_key = api_key
        # Use passed endpoint or default to production endpoint
        self.api_endpoint = api_endpoint or "https://api.microsoftmoderator.com/photodna/v1.0/Match"

    def check_hash(self, file_hash):
        """Send hash to PhotoDNA API and get results"""
        headers = {
            'Content-Type': 'text/plain',  # For CSV hash format
            'Ocp-Apim-Subscription-Key': self.api_key
        }

        try:
            response = requests.post(
                f"{self.api_endpoint}?dataType=Hash",  # Specify we're sending a hash
                headers=headers,
                data=file_hash,  # Send the hash as plain text
                timeout=30
            )

            if response.status_code == 401:
                raise ValueError("Invalid API key - please check your Microsoft PhotoDNA API key")
            elif response.status_code == 429:
                raise ValueError("Rate limit exceeded - please try again later")

            response.raise_for_status()
            result = response.json()

            return {
                'match': result.get('IsMatch', False),
                'details': {
                    'match_flags': result.get('MatchDetails', {}).get('MatchFlags', []),
                    'tracking_id': result.get('TrackingId')
                }
            }

        except requests.exceptions.ConnectionError:
            raise ValueError("Could not connect to Microsoft PhotoDNA API - please check your internet connection")
        except requests.exceptions.Timeout:
            raise ValueError("Request timed out - the API server took too long to respond")
        except requests.exceptions.RequestException as e:
            raise ValueError(f"API request failed: {str(e)}")

    def check_image(self, image_path):
        """Send image to PhotoDNA API and get results"""
        # Get the correct mime type based on file extension
        mime_type, _ = mimetypes.guess_type(image_path)
        if not mime_type or not mime_type.startswith('image/'):
            mime_type = 'application/octet-stream'

        headers = {
            'Content-Type': mime_type,
            'Ocp-Apim-Subscription-Key': self.api_key
        }

        try:
            # For PhotoDNA API, we need to send the actual image data
            with open(image_path, 'rb') as f:
                image_data = f.read()

            print(f"Sending request to PhotoDNA API for {image_path}")
            print(f"Using Content-Type: {mime_type}")

            response = requests.post(
                self.api_endpoint,
                headers=headers,
                data=image_data,
                timeout=30
            )

            print(f"Response status code: {response.status_code}")
            if response.status_code != 200:
                print(f"Error response body: {response.text}")

            if response.status_code == 401:
                raise ValueError("Invalid API key - please check your Microsoft PhotoDNA API key")
            elif response.status_code == 429:
                raise ValueError("Rate limit exceeded - please try again later")

            response.raise_for_status()
            result = response.json()

            print(f"API Response: {result}")

            return {
                'match': result.get('IsMatch', False),
                'details': {
                    'match_flags': result.get('MatchDetails', {}).get('MatchFlags', []),
                    'tracking_id': result.get('TrackingId')
                }
            }

        except requests.exceptions.ConnectionError:
            raise ValueError("Could not connect to Microsoft PhotoDNA API - please check your internet connection")
        except requests.exceptions.Timeout:
            raise ValueError("Request timed out - the API server took too long to respond")
        except requests.exceptions.RequestException as e:
            raise ValueError(f"API request failed: {str(e)}")