from django.forms import (CharField, ChoiceField, DateField, Form, ModelForm,
                          TextInput, BooleanField, DateTimeField, TextInput,
                          FloatField, DecimalField, IntegerField)


class TestSearchForm(Form):
    # TODO: Create a field for ModelChoiceField
    STATUS_CHOICES = [
        ('', 'All'),
        (True, 'Active'),
        (False, 'Inactive')
    ]

    field1 = CharField()
    field2 = TextInput()
    field3 = ChoiceField(choices=STATUS_CHOICES)
    field4 = BooleanField()
    field5 = DateField()
    field6 = DateTimeField()
    field7 = FloatField()
    field8 = DecimalField()
    field9 = IntegerField()

    field90 = CharField()
    field91 = CharField()

    def __init__(self, *args, **kwargs):
        super(TestSearchForm, self).__init__(*args, **kwargs)
        self.fields['field90'].label = "Date Start"
        self.fields['field91'].label = "Date End"
