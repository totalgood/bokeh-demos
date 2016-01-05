from django import forms

from .models import Happiness


class HappinessForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(HappinessForm, self).__init__(*args, **kwargs)
        for field in self.fields.keys():
            # Add bootstrap class
            self.fields[field].widget.attrs['class'] = 'form-control'

    class Meta:
        model = Happiness
        exclude = ('employee',)
