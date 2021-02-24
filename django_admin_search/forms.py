from django import forms


class OverrideSearchForm(forms.Form):
    override = forms.CharField(required=False, widget=forms.TextInput(
        attrs={
            'type': 'text',
            'value': 'Override search_form in your admin.py',
            'disabled': True,
            'style': 'text-align: center'
        }
    ))

    def __init__(self, *args, **kwargs):
        super(OverrideSearchForm, self).__init__(*args, **kwargs)
        self.fields['override'].label = ""
