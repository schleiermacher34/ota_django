# sync_vtiger.py
from django.core.management.base import BaseCommand
from firmware.vtiger_client import VtigerClient
from firmware.models import Machine, User

class Command(BaseCommand):
    help = 'Syncs Vtiger CRM assets with the local database'

    def handle(self, *args, **options):
        # Vtiger CRM credentials and base URL
        base_url = "https://vtiger.anatol.com"
        username = "admin-andrii"
        access_key = "68jhKPOiltQdklnL"  # Replace this with the actual access key

        # Initialize the Vtiger client
        client = VtigerClient(base_url, username, access_key)

        # Login to Vtiger CRM
        client.login()

        # Fetch assets from Vtiger CRM
        assets = client.get_assets()

        # Process each asset
        for asset in assets:
            # Assuming assets have fields: 'asset_name', 'serial_number', 'customer_name', 'product_name'
            asset_name = asset.get('asset_name')
            serial_number = asset.get('serial_number')
            customer_name = asset.get('customer_name')
            product_name = asset.get('product_name')

            # Create or update user in your local database
            user, created = User.objects.get_or_create(username=customer_name)
            if created:
                user.set_password('defaultpassword123')  # Set a default password
                user.save()

            # Create or update machine in your local database
            Machine.objects.update_or_create(
                serial_number=serial_number,
                defaults={
                    'user': user,
                    'model_name': product_name,
                    'asset_name': asset_name,
                }
            )

        print("Synchronization with Vtiger CRM completed successfully.")
