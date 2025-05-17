# django library imports
from django import forms

# project imports
from myapp.models import Publisher


# Create your forms here.
class PublisherForm(forms.ModelForm):
    class Meta:
        model = Publisher
        fields = ['name']
