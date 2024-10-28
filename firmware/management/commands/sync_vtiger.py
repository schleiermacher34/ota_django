# sync_vtiger.py
import json
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from firmware.models import Machine
from firmware.vtiger_client import VtigerClient

class Command(BaseCommand):
    help = 'Synchronize assets from Vtiger CRM with the Django database'

    def handle(self, *args, **options):
        # Initialize Vtiger Client
        base_url = 'https://vtiger.anatol.com'
        username = 'admin-andrii'
        access_key = '68jhKPOiltQdklnL'  # Replace this with your access key
        proxies = {
            "http": None,
            "https": None
        }
        
        client = VtigerClient(base_url, username, access_key, proxies)

        # Attempt to login
        try:
            client.login()
            print("Login successful")
        except Exception as e:
            print(f"An error occurred during login: {e}")
            print("You need to login first.")
            return
        
        # Fetch assets from Vtiger CRM
        assets = client.get_assets()
        if not assets:
            print("No assets fetched.")
            return

        # Process each asset
        for asset in assets:
            print(f"Processing asset: {asset}")  # Debugging line
            
            customer_name = asset.get('customer_name')
            product_name = asset.get('product_name')
            asset_name = asset.get('asset_name')
            serial_number = asset.get('serial_number')

            if not customer_name:
                print(f"Skipping asset due to missing customer name: {asset}")
                # Optionally, log this information to a file for later review
                continue
            
            # Ensure a user exists for the customer
            user, created = User.objects.get_or_create(username=customer_name)
            if created:
                print(f"Created new user for customer: {customer_name}")
            
            # Create or update machine details
            machine, created = Machine.objects.get_or_create(
                serial_number=serial_number,
                defaults={
                    'user': user,
                    'model_name': product_name,
                    'license_key': asset_name,
                }
            )
            
            if created:
                print(f"Added new machine for user {customer_name}: {product_name} - {asset_name}")
            else:
                print(f"Machine already exists for user {customer_name}: {product_name} - {asset_name}")
        
        print("Synchronization with Vtiger CRM completed successfully.")
