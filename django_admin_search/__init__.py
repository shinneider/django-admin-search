# -*- coding: utf-8 -*-
try:
    import django
except ImportError:
    django = None

__version__ = '0.3.10'

if django and django.VERSION < (3, 2):  # pragma: no cover
    default_app_config = 'django_admin_search.apps.DjangoAdminSearchConfig'
