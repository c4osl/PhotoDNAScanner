import requests
import mimetypes

class PhotoDNAClient:
    def __init__(self, api_key, api_endpoint=None):
        self.api_key = api_key
        # Use passed endpoint or default to production endpoint
        self.api_endpoint = api_endpoint or "https://api.microsoftmoderator.com/photodna/v1.0/MatchHash"

    def check_hash(self, file_hash):
        """Send hash to PhotoDNA API and get results"""
        headers = {
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': self.api_key
        }

        try:
            # Format the hash according to API requirements
            data = [{
                "DataRepresentation": "Hash",
                "Value": file_hash
            }]

            print(f"Sending hash request to PhotoDNA API")
            print(f"Request data: {data}")

            response = requests.post(
                self.api_endpoint,
                headers=headers,
                json=data,
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

            # Extract match results from the response
            match_result = result.get('MatchResults', [{}])[0]

            return {
                'match': match_result.get('IsMatch', False),
                'details': {
                    'match_flags': match_result.get('MatchDetails', {}).get('MatchFlags', []),
                    'tracking_id': match_result.get('TrackingId')
                }
            }

        except requests.exceptions.ConnectionError:
            raise ValueError("Could not connect to Microsoft PhotoDNA API - please check your internet connection")
        except requests.exceptions.Timeout:
            raise ValueError("Request timed out - the API server took too long to respond")
        except requests.exceptions.RequestException as e:
            raise ValueError(f"API request failed: {str(e)}")
