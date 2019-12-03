import unittest
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _
from django_admin_search.apps import DjangoAdminSearchConfig

class TestDjangoAppConfig(unittest.TestCase):

    def test_valid_subclass_appconfig(self):
        """
            This project use format major.minor.patch
        """
        self.assertEqual(issubclass(DjangoAdminSearchConfig, AppConfig), True)

    def test_valid_name(self):
        name = DjangoAdminSearchConfig.name
        self.assertEqual(isinstance(name, str), True)
        self.assertEqual(name, 'django_admin_search')

    def test_valid_verbose_name(self):
        verbose_name = DjangoAdminSearchConfig.verbose_name
        self.assertEqual(verbose_name, _('Django Admin Search'))