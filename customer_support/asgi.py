"""
ASGI config for customer_support project.
"""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'customer_support.settings')

application = get_asgi_application()
