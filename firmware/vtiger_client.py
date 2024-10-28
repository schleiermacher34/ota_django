import requests

class VtigerClient:
    def __init__(self, base_url, username, access_key):
        self.base_url = base_url
        self.username = username
        self.access_key = access_key  # Added access_key to the constructor
        self.token = None
        # Ensure the proxy settings are accurate
        self.proxies = {
            "http": "http://admin-andrii:Andrii2024@10.0.4.52:443",
            "https": "https://admin-andrii:Andrii2024@10.0.4.52:443"
        }

    def login(self):
        try:
            # Construct the login URL
            login_url = f"{self.base_url}/webservice.php"

            # Make a request to get a challenge token using the proxy
            token_response = requests.get(login_url, params={
                'operation': 'getchallenge',
                'username': self.username
            }, proxies=self.proxies)

            # Check if the request was successful
            if token_response.status_code == 200:
                response_data = token_response.json()
                if response_data.get('success'):
                    # Successfully retrieved the challenge token
                    self.token = response_data['result']['token']
                    print(f"Challenge Token: {self.token}")
                else:
                    print(f"Error: {response_data['error']['message']}")
            else:
                print(f"Failed to get challenge. Status Code: {token_response.status_code}")

        except requests.RequestException as e:
            print(f"An error occurred: {e}")

    def get_assets(self):
        # This is an example method to fetch assets after successful login
        # Make sure to implement proper API calls as per Vtiger API requirements
        if not self.token:
            print("You need to login first.")
            return []

        try:
            # Example URL for fetching assets - adjust this according to your needs
            assets_url = f"{self.base_url}/webservice.php"
            response = requests.get(assets_url, params={
                'operation': 'listtypes',
                'sessionName': self.token  # Replace with proper session parameter if needed
            }, proxies=self.proxies)

            # Process response
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    print("Assets retrieved successfully.")
                    return data['result']
                else:
                    print(f"Error fetching assets: {data['error']['message']}")
            else:
                print(f"Failed to fetch assets. Status Code: {response.status_code}")

        except requests.RequestException as e:
            print(f"An error occurred: {e}")

        return []
