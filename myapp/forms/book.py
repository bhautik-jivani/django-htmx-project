# django library imports
from django import forms
from django.forms import formset_factory, inlineformset_factory, modelformset_factory

# crispy forms imports
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div, HTML

# project imports
from myapp.models import Book, Person, Publisher

# project forms imports
from myapp.forms.person import PersonForm



# Create your forms here.
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['id', 'name', 'pages', 'price', 'rating', 'persons', 'publisher', 'pubdate']
        widgets = {
            'pubdate': forms.DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['publisher'].label_from_instance = lambda obj: obj.name
