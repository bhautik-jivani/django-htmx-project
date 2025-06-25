# django library imports
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, UpdateView, CreateView
from django.views.generic.edit import FormMixin
from django.urls import reverse_lazy
from django.contrib import messages

# project imports
from myapp.forms import PersonForm
from myapp.models import Person


# Create your views here.
class PersonListView(ListView):
    template_name = 'myapp/person/index.html'
    model = Person
    # context_object_name = 'people'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['person_nav'] = 'active'
        return context

class PersonCreateView(CreateView):
    model = Person
    form_class = PersonForm
    # fields = ['first_name', 'last_name']
    template_name = 'myapp/person/create_form.html'
    success_url = reverse_lazy('myapp:person_list_view')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['person_nav'] = 'active'
        return context

    def form_valid(self, form):
        try:
            print("Form data:", form.cleaned_data)  # Debug print
            response = super().form_valid(form)
            print("Response:", response)  # Debug print
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

class PersonUpdateView(UpdateView):
    pk_url_kwarg = 'pk'
    model = Person
    form_class = PersonForm
    # fields = ['first_name', 'last_name']
    template_name = 'myapp/person/update_form.html'
    success_url = reverse_lazy('myapp:person_list_view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['person_nav'] = 'active'
        return context

    def form_valid(self, form):
        try:
            print("Form data:", form.cleaned_data)  # Debug print
            response = super().form_valid(form)
            print("Response:", response)  # Debug print
            messages.success(self.request, 'Person updated successfully!')
            return response
        except Exception as e:
            print("Error:", str(e))  # Debug print
            messages.error(self.request, f'Error updating person: {str(e)}')
            return self.form_invalid(form)

    def form_invalid(self, form):
        print("Form errors:", form.errors)  # Debug print
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)

