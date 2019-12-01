import django
from django.conf import settings

settings.configure()
settings.INSTALLED_APPS = [
    # Third part apps
    'django_admin_search',
    'test'
]
django.setup()