# django library imports
from django import forms
from django.forms import formset_factory, inlineformset_factory, modelformset_factory

# crispy forms imports
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div, HTML, Row, Column

# project imports
from myapp.models import Store, StoreBook, Book, Person, Publisher

# project forms imports
from myapp.forms.person import PersonForm



# Create your forms here.
class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['id', 'name']


class StoreBookForm(forms.ModelForm):
    class Meta:
        model = StoreBook
        fields = ['id', 'store', 'book', 'price_in_store', 'stock_count']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('book', css_class='col-md-3'),
                Column('price_in_store', css_class='col-md-3'),
                Column('stock_count', css_class='col-md-3'),
            )
        )
    


StoreBookFormSet = inlineformset_factory(
    Store,
    StoreBook,
    form=StoreBookForm,
    extra=1,
    can_delete=True,
)



