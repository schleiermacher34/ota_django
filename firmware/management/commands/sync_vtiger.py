# sync_vtiger.py
# ota_app/management/commands/sync_vtiger.py

import hashlib
import requests
import logging
from django.core.management.base import BaseCommand
from django.conf import settings
from firmware.models import Asset, Customer  # Adjust import paths as necessary

# Configure logging
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Synchronize assets from Vtiger CRM'

    def handle(self, *args, **options):
        # Authenticate with Vtiger
        session_name = self.vtiger_login()
        if not session_name:
            logger.error("Failed to authenticate with Vtiger CRM.")
            return

        # Fetch assets from Vtiger
        vtiger_assets = self.fetch_vtiger_assets(session_name)
        if not vtiger_assets:
            logger.error("No assets fetched from Vtiger CRM.")
            return

        # Cache for product names to minimize API calls
        product_name_cache = {}

        for asset_data in vtiger_assets:
            print(f"Processing asset: {asset_data}")
            account_id = asset_data.get('account')
            product_id = asset_data.get('product')
            customer_name = None
            product_name = None

            # Resolve customer name
            if account_id:
                customer_name = self.get_customer_name_from_vtiger(session_name, account_id)
                if not customer_name:
                    print(f"Skipping asset due to unresolved customer ID: {asset_data}")
                    continue
            else:
                print(f"Skipping asset due to missing account ID: {asset_data}")
                continue

            # Resolve product name
            if product_id:
                product_name = self.get_product_name_from_vtiger(session_name, product_id, product_name_cache)
                if not product_name:
                    print(f"Skipping asset due to unresolved product ID: {asset_data}")
                    continue
            else:
                print(f"Skipping asset due to missing product ID: {asset_data}")
                continue

            # Check if product name contains 'mixer' (case-insensitive)
            if 'tor' in product_name.lower():
                # Proceed to save or update the asset
                self.save_asset(asset_data, customer_name, product_name)
            else:
                print(f"Skipping asset as product '{product_name}' does not contain 'mixer'")
                continue

    def vtiger_login(self):
        """Authenticate with Vtiger and return the session name."""
        vtiger_url = settings.VTIGER_URL
        username = settings.VTIGER_USERNAME
        access_key = settings.VTIGER_ACCESS_KEY

        # Step 1: Get challenge token
        params = {
            'operation': 'getchallenge',
            'username': username,
        }
        try:
            response = requests.get(vtiger_url, params=params)
            data = response.json()
            if data.get('success'):
                token = data['result']['token']
            else:
                logger.error(f"Failed to get challenge token: {data.get('error')}")
                return None

            # Step 2: Login
            key = hashlib.md5((token + access_key).encode('utf-8')).hexdigest()
            params = {
                'operation': 'login',
                'username': username,
                'accessKey': key,
            }
            response = requests.post(vtiger_url, data=params)
            data = response.json()
            if data.get('success'):
                session_name = data['result']['sessionName']
                return session_name
            else:
                logger.error(f"Failed to login: {data.get('error')}")
                return None
        except Exception as e:
            logger.error(f"Exception during Vtiger login: {e}")
            return None

    def fetch_vtiger_assets(self, session_name):
        """Fetch assets from Vtiger CRM."""
        vtiger_url = settings.VTIGER_URL
        params = {
            'operation': 'query',
            'sessionName': session_name,
            'query': "SELECT * FROM Assets;",
        }
        try:
            response = requests.get(vtiger_url, params=params)
            data = response.json()
            if data.get('success'):
                assets = data['result']
                return assets
            else:
                logger.error(f"Failed to fetch assets: {data.get('error')}")
                return []
        except Exception as e:
            logger.error(f"Exception occurred while fetching assets: {e}")
            return []

    def get_customer_name_from_vtiger(self, session_name, account_id):
        """Retrieve the customer name using the account ID."""
        vtiger_url = settings.VTIGER_URL
        params = {
            'operation': 'retrieve',
            'sessionName': session_name,
            'id': account_id,
        }
        try:
            response = requests.get(vtiger_url, params=params)
            data = response.json()

            if data.get('success'):
                account_data = data['result']
                customer_name = account_data.get('accountname')
                return customer_name
            else:
                logger.error(f"Failed to retrieve account {account_id}: {data.get('error')}")
                return None
        except Exception as e:
            logger.error(f"Exception occurred while fetching account {account_id}: {e}")
            return None

    def get_product_name_from_vtiger(self, session_name, product_id, cache):
        """Retrieve the product name using the product ID, with caching."""
        # Check if the product name is already in the cache
        if product_id in cache:
            return cache[product_id]

        vtiger_url = settings.VTIGER_URL
        params = {
            'operation': 'retrieve',
            'sessionName': session_name,
            'id': product_id,
        }
        try:
            response = requests.get(vtiger_url, params=params)
            data = response.json()

            if data.get('success'):
                product_data = data['result']
                product_name = product_data.get('productname')
                # Store in cache
                cache[product_id] = product_name
                return product_name
            else:
                logger.error(f"Failed to retrieve product {product_id}: {data.get('error')}")
                return None
        except Exception as e:
            logger.error(f"Exception occurred while fetching product {product_id}: {e}")
            return None

    def save_asset(self, asset_data, customer_name, product_name):
        """Save or update the asset in the database."""
        # Find or create the customer in your local database
        customer, _ = Customer.objects.get_or_create(name=customer_name)

        # Map asset_data fields to your Asset model fields
        asset_fields = {
            'asset_no': asset_data.get('asset_no'),
            'product': product_name,  # Use product name instead of ID
            'serialnumber': asset_data.get('serialnumber'),
            'datesold': asset_data.get('datesold') or None,
            'dateinservice': asset_data.get('dateinservice') or None,
            'assetstatus': asset_data.get('assetstatus'),
            'assetname': asset_data.get('assetname'),
            'customer': customer,
            # Add other fields as necessary
        }

        # Use unique identifier to find existing asset or create a new one
        asset, created = Asset.objects.update_or_create(
            serialnumber=asset_data.get('serialnumber'),
            defaults=asset_fields,
        )

        if created:
            print(f"Created new asset: {asset}")
        else:
            print(f"Updated existing asset: {asset}")
