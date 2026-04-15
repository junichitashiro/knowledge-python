from django import forms

from sampleapp.models import Sample


class SampleForm(forms.ModelForm):
    class Meta:
        model = Sample
        fields = ('title', 'text')
