# django library imports
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, UpdateView, CreateView
from django.views.generic.edit import FormMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponseForbidden

# project imports
from myapp.forms import PublisherForm
from myapp.models import Publisher


# Create your views here.
class PublisherListView(ListView):
    template_name = 'myapp/publisher/index.html'
    model = Publisher
    # context_object_name = 'people'
    
    # # This is a custom dispatch method(applies to all HTTP methods) to check if the request is an HTMX request
    # def dispatch(self, request, *args, **kwargs):
    #     if request.htmx and request.htmx.request:
    #         return super().dispatch(request, *args, **kwargs)
    #     return HttpResponseForbidden("<h1>Access Denied</h1>")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['publisher_nav'] = 'active'
        return context

class PublisherCreateView(CreateView):
    model = Publisher
    form_class = PublisherForm
    # fields = ['first_name', 'last_name']
    template_name = 'myapp/publisher/create_form.html'
    success_url = reverse_lazy('myapp:publisher_list_view')

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

class PublisherUpdateView(UpdateView):
    pk_url_kwarg = 'pk'
    model = Publisher
    form_class = PublisherForm
    # fields = ['first_name', 'last_name']
    template_name = 'myapp/publisher/update_form.html'
    success_url = reverse_lazy('myapp:publisher_list_view')

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

