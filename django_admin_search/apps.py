# -*- coding: utf-8 -*-
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class DjangoAdminSearchConfig(AppConfig): # Our app config class
    name = 'django_admin_search'
    verbose_name = _('Django Admin Search')