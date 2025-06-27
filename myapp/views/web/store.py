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

# third-party imports
import json


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
        context['store_nav'] = 'active'
        if self.request.POST:
            context['formset'] = StoreBookFormSet(self.request.POST)
        else:
            context['formset'] = StoreBookFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

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
                formset._non_form_errors = formset.non_form_errors() + [f'Error creating store: {str(e)}']
                return self.render_to_response(context)
        else:
            return self.render_to_response(context)


class StoreUpdateView(UpdateView):
    pk_url_kwarg = 'pk'
    model = Store
    form_class = StoreForm
    template_name = 'myapp/store/update_form.html'
    success_url = reverse_lazy('myapp:store_list_view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['store_nav'] = 'active'
        if self.request.POST:
            context['formset'] = StoreBookFormSet(self.request.POST, instance=self.object)
        else:
            context['formset'] = StoreBookFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    # First save the store
                    form.save()
                    # Then set the store on the formset and save it
                    formset.instance = self.object
                    formset.save()
                messages.success(self.request, 'Store updated successfully!')
                return HttpResponseRedirect(self.get_success_url())
            except Exception as e:
                # messages.error(self.request, f'Error updating store: {str(e)}')
                formset._non_form_errors = formset.non_form_errors() + [f'Error updating store: {str(e)}']
                return self.render_to_response(context)
        else:
            return self.render_to_response(context)


class AddBookFormsetView(View):
    # This is a custom dispatch method(applies to all HTTP methods) to check if the request is an HTMX request
    def dispatch(self, request, *args, **kwargs):
        if request.htmx and request.htmx.request:
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseForbidden("<h1>Access Denied</h1>")

    def post(self, request):
        formset = StoreBookFormSet(request.POST)
        initial_form_count = formset.initial_form_count()
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
        formset.management_form.initial["INITIAL_FORMS"] = initial_form_count
        response = render(request, 'myapp/store/partials/add_book_formset.html', {'formset': formset})
        response['HX-Trigger-After-Swap'] = 'update_formset_button'
        return response

class RemoveBookFormsetView(View):
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
        initial_form_count = formset.initial_form_count() - 1 if formset.initial_form_count() > 1 else 0
        # Remove the form at the given index

        form_obj = formset.forms[index]
        id = form_obj.data.get(f"{formset.prefix}-{index}-id")
        if id:
            store_book_queryset = StoreBook.objects.filter(id=id)
            store_book_queryset.delete()
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
        formset.management_form.initial["INITIAL_FORMS"] = initial_form_count
        response = render(request, 'myapp/store/partials/add_book_formset.html', {'formset': formset})
        response['HX-Trigger-After-Swap'] = 'update_formset_button'
        return response
    

class StoreAddBookFormView(CreateView):
    model = Book
    form_class = BookForm
    template_name = 'myapp/store/partials/add_book_form.html'

    # This is a custom dispatch method(applies to all HTTP methods) to check if the request is an HTMX request
    def dispatch(self, request, *args, **kwargs):
        if request.htmx and request.htmx.request:
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseForbidden("<h1>Access Denied</h1>")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['target_formset'] = self.request.GET.get('target_formset', '')
        return context
    
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
            response['HX-Trigger-After-Swap'] = json.dumps({
                'add_book_option_tag': {'option_tag': option_tag,}
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
    
class StoreAddPersonFormView(CreateView):
    model = Person
    form_class = PersonForm
    template_name = 'myapp/store/partials/add_person_form.html'

    def dispatch(self, request, *args, **kwargs):
        if request.htmx and request.htmx.request:
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseForbidden("<h1>Access Denied</h1>")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['target_formset'] = self.request.GET.get('target_formset', '')
        return context
    
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
                "close_offcanvas": {"element_id": "offcanvas-child-1-here"},
            })
            return response
        except Exception as e:
            # messages.error(self.request, f'Error creating person: {str(e)}')
            form.add_error(None, f'Error creating person: {str(e)}')
            print(f"form.errors: {form.errors}")
            response = self.render_to_response(context)
            response['HX-Retarget'] = '#offcanvas-child-1-here'
            response['HX-Reswap'] = 'innerHTML'
            return response

    def form_invalid(self, form):
        # messages.error(self.request, 'Please correct the errors below.')
        context = self.get_context_data(form=form)
        response = self.render_to_response(context)
        response['HX-Retarget'] = '#offcanvas-child-1-here'
        response['HX-Reswap'] = 'innerHTML'
        # response['HX-Trigger-After-Swap'] = 'fail'
        return response

class StoreAddPublisherFormView(CreateView):
    model = Publisher
    form_class = PublisherForm
    template_name = 'myapp/store/partials/add_publisher_form.html'

    def dispatch(self, request, *args, **kwargs):
        if request.htmx and request.htmx.request:
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseForbidden("<h1>Access Denied</h1>")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['target_formset'] = self.request.GET.get('target_formset', '')
        return context
    
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
                "close_offcanvas": {"element_id": "offcanvas-child-1-here"},
            })
            return response
        except Exception as e:
            # messages.error(self.request, f'Error creating person: {str(e)}')
            form.add_error(None, f'Error creating person: {str(e)}')
            print(f"form.errors: {form.errors}")
            response = self.render_to_response(context)
            response['HX-Retarget'] = '#offcanvas-child-1-here'
            response['HX-Reswap'] = 'innerHTML'
            return response

    def form_invalid(self, form):
        # messages.error(self.request, 'Please correct the errors below.')
        context = self.get_context_data(form=form)
        response = self.render_to_response(context)
        response['HX-Retarget'] = '#offcanvas-child-1-here'
        response['HX-Reswap'] = 'innerHTML'
        # response['HX-Trigger-After-Swap'] = 'fail'
        return response