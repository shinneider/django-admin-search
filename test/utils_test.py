import unittest
from datetime import date, datetime
from decimal import Decimal
from django_admin_search.utils import format_data
from django import forms
from django.db import models
from django.core.exceptions import ValidationError
from django_mock_queries.query import MockSet, MockModel


class TestUtilsFunctions(unittest.TestCase):

    def test_char_field_parse(self):
        field = forms.CharField()
        self.assertEqual(format_data(field, '1'), '1')
        self.assertEqual(format_data(field, 1), '1')
        self.assertEqual(format_data(field, False), 'False')
        self.assertEqual(format_data(field, 0), '0')
        self.assertEqual(format_data(field, '%20F'), '%20F')
        self.assertRaises(ValidationError, lambda: format_data(field, ' '))

    def test_text_field_parse(self):
        field = forms.TextInput()
        self.assertEqual(format_data(field, '1'), '1')
        self.assertEqual(format_data(field, 1), '1')
        self.assertEqual(format_data(field, False), 'False')
        self.assertEqual(format_data(field, 0), '0')
        self.assertEqual(format_data(field, '%20F'), '%20F')
        self.assertEqual(format_data(field, ' '), ' ')

    def test_choice_field_parse(self):
        field = forms.ChoiceField(choices=[(True, 'True'), (False, 'False')])
        self.assertEqual(format_data(field, True), True)
        self.assertEqual(format_data(field, False), False)
        self.assertRaises(ValidationError, lambda: format_data(field, 1))
        self.assertRaises(ValidationError, lambda: format_data(field, 0))
        self.assertRaises(ValidationError, lambda: format_data(field, 'true'))
        self.assertRaises(ValidationError, lambda: format_data(field, 'false'))

    def test_model_choice_field_parse(self):
        qs = MockSet(MockModel(pk=0), MockModel(pk=1), MockModel(pk=2))
        field = forms.ModelChoiceField(queryset=qs)
        
        self.assertEqual(format_data(field, 0), 0)
        self.assertEqual(format_data(field, 1), 1)
        self.assertEqual(format_data(field, 2), 2)
        self.assertRaises(AttributeError, lambda: format_data(field, 4))

    def test_boolean_field_parse(self):
        field = forms.BooleanField()
        self.assertEqual(format_data(field, True), True)
        self.assertEqual(format_data(field, 1), True)
        self.assertEqual(format_data(field, '1'), True)
        self.assertEqual(format_data(field, False), False)
        self.assertEqual(format_data(field, 0), False)
        self.assertEqual(format_data(field, ''), False)

    def test_float_field_parse(self):
        field = forms.FloatField()
        self.assertEqual(format_data(field, 1), 1.0)
        self.assertEqual(format_data(field, '1'), 1.0)
        self.assertEqual(format_data(field, 0), 0.0)
        self.assertEqual(format_data(field, '0'), 0.0)

    def test_decimal_field_parse(self):
        field = forms.DecimalField()

        self.assertEqual(format_data(field, 1), 1.0)
        self.assertEqual(isinstance(format_data(field, 1), Decimal), True)

        self.assertEqual(format_data(field, '1'), 1.0)
        self.assertEqual(isinstance(format_data(field, '1'), Decimal), True)

        self.assertEqual(format_data(field, 0), 0.0)
        self.assertEqual(isinstance(format_data(field, 0), Decimal), True)

        self.assertEqual(format_data(field, '0'), 0.0)
        self.assertEqual(isinstance(format_data(field, '0'), Decimal), True)

    def test_integer_field_parse(self):
        field = forms.IntegerField()

        self.assertEqual(format_data(field, 1), 1)
        self.assertEqual(format_data(field, '1'), 1)
        self.assertEqual(format_data(field, '0'), 0)
        self.assertRaises(ValidationError, lambda: format_data(field, 1.1))

    def test_date_field_parse(self):
        field = forms.DateField()
        self.assertEqual(format_data(field, '06/26/1997'), date(1997, 6, 26))
        self.assertRaises(ValidationError, lambda: format_data(field, ''))
        self.assertRaises(AttributeError, lambda: format_data(field, 1))

    def test_datetime_field_parse(self):
        field = forms.DateTimeField()
        self.assertEqual(format_data(field, '06/26/1997'), datetime(1997, 6, 26))
        self.assertEqual(format_data(field, '06/26/1997 3:0:0'), datetime(1997, 6, 26, 3, 0, 0))
        self.assertRaises(ValidationError, lambda: format_data(field, ''))
        self.assertRaises(AttributeError, lambda: format_data(field, 1))
