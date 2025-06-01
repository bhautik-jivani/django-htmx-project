# django library imports
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, UpdateView, CreateView, View
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponseForbidden, HttpResponse
from django.db import transaction

# project imports
from myapp.forms import StoreForm, StoreBookFormSet, BookForm, PersonForm, PublisherForm
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
    template_name = 'myapp/store/create_form.html'
    success_url = reverse_lazy('myapp:store_list_view')

    # # This is a custom dispatch method(applies to all HTTP methods) to check if the request is an HTMX request
    # def dispatch(self, request, *args, **kwargs):
    #     if request.htmx and request.htmx.request:
    #         return super().dispatch(request, *args, **kwargs)
    #     return HttpResponseForbidden("<h1>Access Denied</h1>")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = StoreBookFormSet(self.request.POST, instance=self.object)
        else:
            context['formset'] = StoreBookFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        print(f"Form data: {form.cleaned_data}")
        print(f"Context: {context}")
        formset = context['formset']
        print(f"Formset: {formset.cleaned_data}")
        try:
            if formset.is_valid():
                with transaction.atomic():
                    # First save the store
                    self.object = form.save()
                    # Then set the store on the formset and save it
                    formset.instance = self.object
                    formset.save()
                messages.success(self.request, 'Store created successfully!')
                return super().form_valid(form)
            else:
                return self.render_to_response(self.get_context_data(form=form))
        except Exception as e:
            print(f"Error: {e}")
            messages.error(self.request, f'Error creating store: {str(e)}')
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


class AddBookFormView(View):
    def get(self, request):
        index = request.GET.get('index', 0)
        try:
            index = int(index)
        except ValueError:
            index = 0
        formset = StoreBookFormSet()
        form = formset.empty_form
        form.prefix = f"{formset.prefix}-{index}"
        response = render(request, 'myapp/store/add_book_form.html', {'form': form})
        response['HX-Trigger-After-Swap'] = 'update_formset_count'
        return response
