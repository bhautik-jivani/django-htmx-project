# django library imports
from django import forms

# project imports
from myapp.models import Person


# Create your forms here.
class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'role']
