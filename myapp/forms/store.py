# django library imports
from django import forms
from django.forms import formset_factory, inlineformset_factory, modelformset_factory

# crispy forms imports
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div, HTML

# project imports
from myapp.models import Store, Book, Person, Publisher

# project forms imports
from myapp.forms.person import PersonForm



# Create your forms here.
class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['id', 'name']

