import unittest
from django.db.models import Q
from django.contrib import messages
from django_admin_search.admin import AdvancedSearchAdmin
from django_mock_queries.query import MockSet, MockModel
from unittest.mock import patch
from django.contrib.admin.sites import AdminSite
from django.http.request import HttpRequest
from django.contrib.messages.storage.fallback import FallbackStorage


class TestAdminOverride(unittest.TestCase):
    qs = MockSet(MockModel(pk=0, name='test1'), MockModel(pk=1, name='test2'), 
                 MockModel(pk=2, name='test3'))
    
    @patch.object(AdvancedSearchAdmin, 'advanced_search_query')
    @patch('django_admin_search.admin.super')
    def test_get_queryset(self, admin_super, mock_advanced_search_query):
        admin_super().get_queryset.return_value = self.qs
        mock_advanced_search_query.return_value = ~Q(pk=99)

        admin = AdvancedSearchAdmin(model=MockModel, admin_site=AdminSite())

        result = admin.get_queryset({})
        self.assertEqual(result.count(), self.qs.count())

    @patch.object(AdvancedSearchAdmin, 'advanced_search_query')
    @patch('django_admin_search.admin.super')
    def test_get_queryset_by_pk(self, admin_super, mock_advanced_search_query):
        admin_super().get_queryset.return_value = self.qs
        mock_advanced_search_query.return_value = ~Q(pk=2)

        admin = AdvancedSearchAdmin(model=MockModel, admin_site=AdminSite())

        result = admin.get_queryset({})
        self.assertEqual(result.count(), 2)

    @patch.object(AdvancedSearchAdmin, 'advanced_search_query')
    @patch('django_admin_search.admin.super')
    def test_get_queryset_erro_message(self, admin_super, mock_advanced_search_query):
        admin_super().get_queryset.return_value = self.qs
        mock_advanced_search_query.side_effect = Exception('example')

        admin = AdvancedSearchAdmin(model=MockModel, admin_site=AdminSite())
        request = HttpRequest()
        setattr(request, 'session', 'session')
        setattr(request, '_messages', FallbackStorage(request))

        self.assertEqual(admin.get_queryset(request).count(), 0)

        msgs = list(messages.get_messages(request))
        self.assertEqual(len(msgs), 1)
        self.assertEqual(msgs[0].level_tag, 'error')
        self.assertEqual(msgs[0].message, 'Filter not applied, error has occurred')