from django import forms
from django.utils import timezone
from django.conf import settings as s
from django.utils.formats import get_format


def format_data(value, key_value):
    """
    Return data converted by form type
    """
    if isinstance(value, forms.CharField) or isinstance(value, forms.TextInput) or \
       isinstance(value, forms.BooleanField) or isinstance(value, forms.ChoiceField) or \
       isinstance(value, forms.ModelChoiceField):

        return key_value

    if isinstance(value, forms.FloatField):
        return float(key_value)

    if isinstance(value, forms.IntegerField):
        return int(key_value)

    if isinstance(value, forms.DateField):
        return parse_date(key_value, 'DATE_INPUT_FORMATS')

    if isinstance(value, forms.DateTimeField):
        return parse_date(key_value, 'DATETIME_INPUT_FORMATS')

    raise Exception


def parse_date(date_str, input_format):
    """
    Parse date by django date and datetime formats
    https://docs.djangoproject.com/en/2.0/ref/settings/#date-input-formats
    https://docs.djangoproject.com/en/2.0/ref/settings/#datetime-input-formats
    """
    for item in get_format(input_format):
        try:
            return timezone.datetime.strptime(date_str, item).date()
        except (ValueError, TypeError):
            continue

    raise Exception