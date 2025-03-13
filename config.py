import os
import configparser

class Config:
    def __init__(self, config_path):
        self.config_path = config_path
        self.config = configparser.ConfigParser()

        # Create config directory if it doesn't exist
        os.makedirs(os.path.dirname(config_path), exist_ok=True)

        # Load or create config file
        if os.path.exists(config_path):
            self.config.read(config_path)
        else:
            self._create_default_config()

    def _create_default_config(self):
        """Create default configuration file"""
        self.config['PhotoDNA'] = {
            'api_key': os.getenv('PHOTODNA_API_KEY', ''),
            'api_endpoint': 'https://api.microsoftmoderator.com/photodna/v1.0/MatchHash'
        }

        # Write config file
        with open(self.config_path, 'w') as config_file:
            self.config.write(config_file)

    def get_api_key(self):
        """Get API key from config or environment"""
        api_key = os.getenv('PHOTODNA_API_KEY')
        if api_key:
            return api_key

        try:
            api_key = self.config['PhotoDNA']['api_key']
            if not api_key:
                raise ValueError("PhotoDNA API key not found. Please set it in the config file or PHOTODNA_API_KEY environment variable")
            return api_key
        except (KeyError, configparser.NoSectionError):
            raise ValueError("PhotoDNA API key not found. Please set it in the config file or PHOTODNA_API_KEY environment variable")

    def get_api_endpoint(self):
        """Get API endpoint from config"""
        try:
            return self.config['PhotoDNA']['api_endpoint']
        except (KeyError, configparser.NoSectionError):
            return 'https://api.microsoftmoderator.com/photodna/v1.0/MatchHash'