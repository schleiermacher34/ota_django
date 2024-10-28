"""
WSGI config for ota_server project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
import sys

# Add the project directory to the system path
project_home = '/home/schleiermacher34/ota_server'  # Replace with the correct path to your project
if project_home not in sys.path:
    sys.path.insert(0, project_home)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ota_server.settings')

# Activate virtual environment (only if using a virtual environment)
activate_this = '/home/schleiermacher34/.virtualenvs/myenv/bin/activate_this.py'
exec(open(activate_this).read(), {'__file__': activate_this})

# Import Django WSGI handler
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

