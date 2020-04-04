from django import forms


def format_data(value, key_value):
    """
    Return data converted by form type
    """
    if isinstance(value, (forms.ChoiceField, forms.ModelChoiceField)):
        value.clean(key_value)
        return key_value

    elif isinstance(value, forms.TextInput):
        return str(key_value)

    elif isinstance(value, forms.BooleanField):
        # in case you have doubts (because i find it very strange)
        # see a ticket https://code.djangoproject.com/ticket/31049
        return bool(key_value)

    else:
        return value.clean(key_value)
