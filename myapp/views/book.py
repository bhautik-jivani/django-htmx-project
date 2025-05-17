# django library imports
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, UpdateView, CreateView, View
from django.views.generic.list import MultipleObjectMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponseForbidden

# project imports
from myapp.forms import BookForm, PersonFormSet, PersonForm
from myapp.models import Book, Person


# Create your views here.
class BookListView(ListView):
    template_name = 'myapp/book/index.html'
    model = Book

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book_nav'] = 'active'
        return context

class BookCreateView(CreateView):
    model = Book
    form_class = BookForm
    # fields = ['first_name', 'last_name']
    template_name = 'myapp/book/create_form.html'
    success_url = reverse_lazy('myapp:book_list_view')

    # # This is a custom dispatch method(applies to all HTTP methods) to check if the request is an HTMX request
    # def dispatch(self, request, *args, **kwargs):
    #     if request.htmx and request.htmx.request:
    #         return super().dispatch(request, *args, **kwargs)
    #     return HttpResponseForbidden("<h1>Access Denied</h1>")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['person_formset'] = PersonFormSet(self.request.POST, queryset=Person.objects.none())
        else:
            context['person_formset'] = PersonFormSet(queryset=Person.objects.none())
        return context




    def form_valid(self, form):
        context = self.get_context_data()
        try:
            print("Form data:", form.cleaned_data)  # Debug print
            person_formset = context['person_formset']
            response = super().form_valid(form)
            print("Response:", response)  # Debug print
            if person_formset.is_valid():
                person_formset.instance = self.object
                person_formset.save()
            else:
                self.object.delete()
                messages.error(self.request, 'Person creation failed!')
                return self.form_invalid(form)
            messages.success(self.request, 'Person created successfully!')
            return response
        except Exception as e:
            print("Error:", str(e))  # Debug print
            messages.error(self.request, f'Error creating person: {str(e)}')
            return self.form_invalid(form)

    def form_invalid(self, form):
        print("Form errors:", form.errors)  # Debug print
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)

class BookUpdateView(UpdateView):
    pk_url_kwarg = 'pk'
    model = Book
    form_class = BookForm
    # fields = ['first_name', 'last_name']
    template_name = 'myapp/book/update_form.html'
    success_url = reverse_lazy('myapp:book_list_view')

    # # This is a custom dispatch method(applies to all HTTP methods) to check if the request is an HTMX request
    # def dispatch(self, request, *args, **kwargs):
    #     if request.htmx and request.htmx.request:
    #         return super().dispatch(request, *args, **kwargs)
    #     return HttpResponseForbidden("<h1>Access Denied</h1>")

    def form_valid(self, form):
        try:
            print("Form data:", form.cleaned_data)  # Debug print
            response = super().form_valid(form)
            print("Response:", response)  # Debug print
            messages.success(self.request, 'Publisher created successfully!')
            return response
        except Exception as e:
            print("Error:", str(e))  # Debug print
            messages.error(self.request, f'Error creating publisher: {str(e)}')
            return self.form_invalid(form)

    def form_invalid(self, form):
        print("Form errors:", form.errors)  # Debug print
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)


class AddPersonFormView(CreateView):
    model = Person
    form_class = PersonForm
    template_name = 'myapp/book/partials/person_form.html'

    # This is a custom dispatch method(applies to all HTTP methods) to check if the request is an HTMX request
    def dispatch(self, request, *args, **kwargs):
        if request.htmx and request.htmx.request:
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseForbidden("<h1>Access Denied</h1>")
    
    def form_valid(self, form):
        try:
            # Save the form but don't redirect
            self.object = form.save()
            messages.success(self.request, 'Person created successfully!')
            
            # Add the updated person list to the context
            context = self.get_context_data()
            context['persons'] = Person.objects.all()
            context['form'] = form
            context['object'] = self.object
            
            return self.render_to_response(context)
        except Exception as e:
            messages.error(self.request, f'Error creating person: {str(e)}')
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)



