# django library imports
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, UpdateView, CreateView, View
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponseForbidden, HttpResponse

# project imports
from myapp.forms import BookForm, PersonForm, PublisherForm
from myapp.models import Book, Person, Publisher

# third party library imports
import json


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

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        try:
            response = super().form_valid(form)
            messages.success(self.request, 'Book created successfully!')
            return response
        except Exception as e:
            # messages.error(self.request, f'Error creating book: {str(e)}')
            form.add_error(None, f'Error creating book: {str(e)}')
            return self.render_to_response(context)

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
        context = self.get_context_data(form=form)
        try:
            response = super().form_valid(form)
            messages.success(self.request, 'Book updated successfully!')
            return response
        except Exception as e:
            # messages.error(self.request, f'Error updating book: {str(e)}')
            form.add_error(None, f'Error updating book: {str(e)}')
            return self.render_to_response(context)

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
        context = self.get_context_data(form=form)
        try:
            # Save the form but don't redirect
            self.object = form.save()
            # messages.success(self.request, 'Person created successfully!')
            
            # Add option tag directly as OOB swap
            option_tag = f'<option value="{self.object.id}" selected>{self.object}</option>'
            response = HttpResponse(option_tag)
            response['HX-Trigger'] = json.dumps({
                "close_offcanvas": {"element_id": "offcanvas-here"},
            })
            return response
        except Exception as e:
            # messages.error(self.request, f'Error creating person: {str(e)}')
            form.add_error(None, f'Error creating person: {str(e)}')
            print(f"form.errors: {form.errors}")
            response = self.render_to_response(context)
            response['HX-Retarget'] = '#offcanvas-here'
            response['HX-Reswap'] = 'innerHTML'
            return response

    def form_invalid(self, form):
        # messages.error(self.request, 'Please correct the errors below.')
        context = self.get_context_data(form=form)
        response = self.render_to_response(context)
        response['HX-Retarget'] = '#offcanvas-here'
        response['HX-Reswap'] = 'innerHTML'
        # response['HX-Trigger-After-Swap'] = 'fail'
        return response

class AddPublisherFormView(CreateView):
    model = Publisher
    form_class = PublisherForm
    template_name = 'myapp/book/partials/publisher_form.html'

    # This is a custom dispatch method(applies to all HTTP methods) to check if the request is an HTMX request
    def dispatch(self, request, *args, **kwargs):
        if request.htmx and request.htmx.request:
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseForbidden("<h1>Access Denied</h1>")
    
    def form_valid(self, form):
        context = self.get_context_data(form=form)
        try:
            # Save the form but don't redirect
            self.object = form.save()
            # messages.success(self.request, 'Publisher created successfully!')
            
            # Add option tag directly as OOB swap
            option_tag = f'<option value="{self.object.id}" selected>{self.object.name}</option>'
            response = HttpResponse(option_tag)
            response['HX-Trigger'] = json.dumps({
                "close_offcanvas": {"element_id": "offcanvas-here"},
            })
            return response
        except Exception as e:
            # messages.error(self.request, f'Error creating publisher: {str(e)}')
            form.add_error(None, f'Error creating publisher: {str(e)}')
            response = self.render_to_response(context)
            response['HX-Retarget'] = '#offcanvas-here'
            response['HX-Reswap'] = 'innerHTML'
            return response

    def form_invalid(self, form):
        # messages.error(self.request, 'Please correct the errors below.')
        context = self.get_context_data(form=form)
        response = self.render_to_response(context)
        response['HX-Retarget'] = '#offcanvas-here'
        response['HX-Reswap'] = 'innerHTML'
        return response

