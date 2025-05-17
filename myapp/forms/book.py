# django library imports
from django import forms
from django.forms import formset_factory, inlineformset_factory, modelformset_factory

# project imports
from myapp.models import Book, Person

# project forms imports
from myapp.forms.person import PersonForm



# Create your forms here.
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['id', 'name', 'pages', 'price', 'rating', 'persons', 'publisher', 'pubdate']


# Create an inline formset for adding multiple persons to a book
PersonFormSet = modelformset_factory(Person, form=PersonForm, extra=1, can_delete=True)

