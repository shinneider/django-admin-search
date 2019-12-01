from django import forms


def format_data(value, key_value):
    """
    Return data converted by form type
    """
    if isinstance(value, forms.ChoiceField) or isinstance(value, forms.ModelChoiceField):
        value.clean(key_value)
        return key_value

    elif isinstance(value, forms.TextInput):
        return str(key_value)

    elif isinstance(value, forms.BooleanField):
        """
            this is a erro in django :o
            forms.BooleanField().validate(value=False) generate a erro,
            but 'False' is a valid value for BooleanField
            I opened a ticket https://code.djangoproject.com/ticket/31049
            after resolution, exclude this section
        """
        return bool(key_value)

    else:
        return value.clean(key_value)