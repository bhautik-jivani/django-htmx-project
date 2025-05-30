# django library imports
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, UpdateView, CreateView, View
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponseForbidden, HttpResponse

# project imports
from myapp.forms import StoreForm, BookForm, PersonForm, PublisherForm
from myapp.models import Book, Person, Publisher, Store


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
    # fields = ['first_name', 'last_name']
    template_name = 'myapp/store/create_form.html'
    success_url = reverse_lazy('myapp:store_list_view')

    # # This is a custom dispatch method(applies to all HTTP methods) to check if the request is an HTMX request
    # def dispatch(self, request, *args, **kwargs):
    #     if request.htmx and request.htmx.request:
    #         return super().dispatch(request, *args, **kwargs)
    #     return HttpResponseForbidden("<h1>Access Denied</h1>")

    def form_valid(self, form):
        context = self.get_context_data()
        try:
            print("Form data:", form.cleaned_data)  # Debug print
            response = super().form_valid(form)
            print("Response:", response)  # Debug print
            
            messages.success(self.request, 'Book created successfully!')
            return response
        except Exception as e:
            print("Error:", str(e))  # Debug print
            messages.error(self.request, f'Error creating book: {str(e)}')
            return self.form_invalid(form)

    def form_invalid(self, form):
        print("Form errors:", form.errors)  # Debug print
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)

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