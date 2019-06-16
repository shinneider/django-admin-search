from django.forms import (CharField, ChoiceField, DateField, Form, ModelForm,
                          TextInput)

from .models import Area


class AreaSearchForm(Form):
    STATUS_CHOICES = [
        ('', 'All'),
        (True, 'Active'),
        (False, 'Inactive')
    ]

    name = CharField(required=False, widget=TextInput(
        attrs={
            'filter_method': '__contains',
        }
    ))
    active = ChoiceField(choices=STATUS_CHOICES, required=False)
    description = CharField(required=False)
    begin = DateField(required=False, widget=TextInput(
        attrs={
            'filter_field': 'date',
            'filter_method': '__gte',
            'data-mask': "00/00/0000",
            'placeholder': 'MM/DD/YYYY'
        }
    ))
    end = DateField(required=False, widget=TextInput(
        attrs={
            'filter_field': 'date',
            'filter_method': '__lte',
            'data-mask': "00/00/0000",
            'placeholder': 'MM/DD/YYYY'
        }
    ))

    def __init__(self, *args, **kwargs):
        super(AreaSearchForm, self).__init__(*args, **kwargs)
        self.fields['begin'].label = "Date Start"
        self.fields['end'].label = "Date End"


class AreaForm(ModelForm):
    class Meta:
        model = Area
        fields = '__all__'
