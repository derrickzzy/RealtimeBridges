from django import forms
from django.forms import ModelForm
from server.models import Bridge
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class BridgeForm(ModelForm):
    class Meta:
        model = Bridge
        fields = ['name', 'number', 'year', 'inspection','town','state']

    def __init__(self, *args, **kwargs):
        super(BridgeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-offset-1 col-sm-2'
        self.helper.field_class = 'col-sm-8'
        self.helper.add_input(Submit('submit', 'Submit'))


class EventForm(forms.Form):
    bridgenumber = forms.CharField(max_length=10)
    eventfile = forms.FileField()
