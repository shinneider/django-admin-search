from .models import Area
from django.forms import ModelForm, Form
from django.forms import DateField, CharField, ChoiceField, TextInput


class AreaSearchForm(Form):
    STATUS_CHOICES = [
        ('', 'All'),
        (True, 'Active'),
        (False, 'Inactive')
    ]

    name = CharField(required=False)
    active = ChoiceField(choices=STATUS_CHOICES, required=False)
    description = CharField(required=False)
    begin = DateField(required=False, widget=TextInput(attrs={'data_filter': '__gte'}))
    end = DateField(required=False, widget=TextInput(attrs={'data_filter': '__lte'}))

class AreaForm(ModelForm):
    class Meta:
        model = Area
        fields = '__all__'
