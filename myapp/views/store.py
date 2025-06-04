# django library imports
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, UpdateView, CreateView, View
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponseForbidden, HttpResponseRedirect, HttpResponse
from django.db import transaction
from django.forms import inlineformset_factory

# project imports
from myapp.forms import StoreForm, StoreBookFormSet, StoreBookForm, BookForm, PersonForm, PublisherForm
from myapp.models import Book, Person, Publisher, Store, StoreBook


# Create your views here.
class StoreListView(ListView):
    template_name = 'myapp/store/index.html'
    model = Store

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['store_nav'] = 'active'
        return context

class StoreCreateView(CreateView):
    model = Store
    form_class = StoreForm
    template_name = 'myapp/store/create_form.html'
    success_url = reverse_lazy('myapp:store_list_view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        index = self.request.POST.get('index', 0)
        try:
            index = int(index)
        except ValueError:
            index = 0
        context['index'] = index
        if self.request.POST:
            print("self.request.POST", self.request.POST)
            context['formset'] = StoreBookFormSet(self.request.POST)
        else:
            context['formset'] = StoreBookFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        print(f"INSIDE:form_valid:formset.is_valid(): {formset.is_valid()}")

        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    # First save the store
                    self.object = form.save()
                    # Then set the store on the formset and save it
                    formset.instance = self.object
                    formset.save()
                messages.success(self.request, 'Store created successfully!')
                return HttpResponseRedirect(self.get_success_url())
            except Exception as e:
                print(f"Error: {e}")
                # messages.error(self.request, f'Error creating store: {str(e)}')
                return self.form_invalid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        context = self.get_context_data()  # Debug print
        formset = context['formset']
        print(f"formset.errors: {formset.errors}")
        print(f"INSIDE:form_invalid:formset.is_valid(): {formset.is_valid()}")
        # messages.error(self.request, 'Please correct the errors below.')
        return self.render_to_response(context)

# class BookUpdateView(UpdateView):
#     pk_url_kwarg = 'pk'
#     model = Book
#     form_class = BookForm
#     # fields = ['first_name', 'last_name']
#     template_name = 'myapp/book/update_form.html'
#     success_url = reverse_lazy('myapp:book_list_view')

#     # # This is a custom dispatch method(applies to all HTTP methods) to check if the request is an HTMX request
#     # def dispatch(self, request, *args, **kwargs):
#     #     if request.htmx and request.htmx.request:
#     #         return super().dispatch(request, *args, **kwargs)
#     #     return HttpResponseForbidden("<h1>Access Denied</h1>")

#     def form_valid(self, form):
#         try:
#             print("Form data:", form.cleaned_data)  # Debug print
#             response = super().form_valid(form)
#             print("Response:", response)  # Debug print
#             messages.success(self.request, 'Book updated successfully!')
#             return response
#         except Exception as e:
#             print("Error:", str(e))  # Debug print
#             messages.error(self.request, f'Error creating book: {str(e)}')
#             return self.form_invalid(form)

#     def form_invalid(self, form):
#         print("Form errors:", form.errors)  # Debug print
#         messages.error(self.request, 'Please correct the errors below.')
#         return super().form_invalid(form)


class AddBookFormView(View):
    # This is a custom dispatch method(applies to all HTTP methods) to check if the request is an HTMX request
    def dispatch(self, request, *args, **kwargs):
        if request.htmx and request.htmx.request:
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseForbidden("<h1>Access Denied</h1>")

    def post(self, request):
        formset = StoreBookFormSet(request.POST)
        inital_data = []
        for form in formset.forms:
            data = {}
            for field in form:
                if field.name != 'DELETE':
                    data[field.name] = field.data
            inital_data.append(data)
        extra = len(inital_data)
        StoreBookFormSet_Custom = inlineformset_factory(
            Store,
            StoreBook,
            form=StoreBookForm,
            extra=extra,
            min_num=1,
            max_num=3,
            validate_min=True,
            validate_max=True,
            can_delete=True,
        )
        formset = StoreBookFormSet_Custom(initial=inital_data)
        response = render(request, 'myapp/store/partials/add_book_formset.html', {'formset': formset})
        response['HX-Trigger-After-Swap'] = 'update_formset_button'
        return response

class RemoveBookFormView(View):
    # This is a custom dispatch method(applies to all HTTP methods) to check if the request is an HTMX request
    def dispatch(self, request, *args, **kwargs):
        if request.htmx and request.htmx.request:
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseForbidden("<h1>Access Denied</h1>")

    def post(self, request):
        index = request.POST.get('index', 0)
        try:
            index = int(index)
        except ValueError:
            index = 0
        formset = StoreBookFormSet(request.POST)
        # Remove the form at the given index
        formset.forms.pop(index)

        inital_data = []
        for form in formset.forms:
            data = {}
            for field in form:
                data[field.name] = field.data
            inital_data.append(data)
        
        extra = len(inital_data) - 1 if len(inital_data) > 1 else 0
        StoreBookFormSet_Custom = inlineformset_factory(
            Store,
            StoreBook,
            form=StoreBookForm,
            extra=extra,
            min_num=1,
            max_num=3,
            validate_min=True,
            validate_max=True,
            can_delete=True,
        )
        formset = StoreBookFormSet_Custom(initial=inital_data)
        response = render(request, 'myapp/store/partials/add_book_formset.html', {'formset': formset})
        response['HX-Trigger-After-Swap'] = 'update_formset_button'
        return response