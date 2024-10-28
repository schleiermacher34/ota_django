import requests
import hashlib

class VtigerClient:
    def __init__(self, base_url, username, access_key, proxies=None):
        self.base_url = base_url
        self.username = username
        self.access_key = access_key
        self.token = None  # Initialize the token attribute
        self.proxies = proxies

    def login(self):
        # Example login URL
        login_url = f"{self.base_url}/webservice.php"
        try:
            # Fetch challenge token
            token_response = requests.get(
                login_url,
                params={'operation': 'getchallenge', 'username': self.username},
                proxies=self.proxies,
                timeout=10
            )
            token_response.raise_for_status()
            token_data = token_response.json()

            if token_data['success']:
                # Store the challenge token securely
                challenge_token = token_data['result']['token']
                
                # Hash the challenge token with your access_key
                key = hashlib.md5((challenge_token + self.access_key).encode('utf-8')).hexdigest()

                # Authenticate with the hashed key
                auth_response = requests.post(
                    login_url,
                    data={
                        'operation': 'login',
                        'username': self.username,
                        'accessKey': key
                    },
                    proxies=self.proxies,
                    timeout=10
                )
                auth_response.raise_for_status()
                auth_data = auth_response.json()

                if auth_data['success']:
                    print("Login successful")
                    # Save the session token for future requests
                    self.token = auth_data['result']['sessionName']
                else:
                    print("Authentication failed")
            else:
                print("Challenge request failed")
        except Exception as e:
            print(f"An error occurred during login: {e}")

    def get_assets(self):
        # Ensure that the login was successful before making requests
        if not self.token:
            print("You need to login first.")
            return None
        
        assets_url = f"{self.base_url}/webservice.php"
        try:
            assets_response = requests.get(
                assets_url,
                params={
                    'operation': 'query',
                    'sessionName': self.token,
                    'query': 'SELECT * FROM Assets;'
                },
                proxies=self.proxies,
                timeout=10
            )
            assets_response.raise_for_status()
            assets_data = assets_response.json()
            
            if assets_data['success']:
                return assets_data['result']
            else:
                print("Failed to fetch assets")
                return None
        except Exception as e:
            print(f"An error occurred while fetching assets: {e}")
            return None
