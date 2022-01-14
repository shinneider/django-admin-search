from django import forms


def format_data(value, key_value):
    """
    Return data converted by form type
    """
    result = None
    if isinstance(value, (forms.ChoiceField, forms.ModelChoiceField)):
        value.clean(key_value)
        result = key_value

    elif isinstance(value, forms.TextInput):
        result = str(key_value)

    elif isinstance(value, forms.BooleanField):
        # in case you have doubts (because i find it very strange)
        # see a ticket https://code.djangoproject.com/ticket/31049
        result = bool(key_value)

    else:
        result = value.clean(key_value)

    return result
