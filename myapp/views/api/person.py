# django libraries import
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Q, F, Sum, Case, When
from django.db import models
from django.views import View

# project models import
from myapp.models import Person  # Replace with your actual model

# Create your views here.
class PersonAPIView(View):

    def get(self, request, *args, **kwargs):
        draw = int(request.GET.get("draw", 1))  # Required for DataTables
        search_query = request.GET.get("search", "").strip()  # DataTables uses "search[value]"
        start = int(request.GET.get("start", 0))  # Offset for pagination
        length = int(request.GET.get("length", 10))  # Number of records per page

        order_column_index = int(request.GET.get("order_column", 1))  # Default to column index 1
        order_dir = request.GET.get("order_dir", "asc")

        # Mapping DataTables column index to model field names
        column_mapping = {
            1: "id",
            2: "first_name",
            3: "last_name",
            4: "role",
        }

        # Default sorting column
        order_column = column_mapping.get(order_column_index, "id")

        # Apply sorting direction
        if order_dir == "desc":
            order_column = f"-{order_column}"  # Add '-' for descending order

        if length > 50:  # Enforce max limit
            length = 50

        # Apply search filter (adjust fields based on your model)
        person_queryset = Person.objects.all()
        if search_query:
            person_queryset = person_queryset.filter(
                Q(id__icontains=search_query) | 
                Q(first_name__icontains=search_query) | 
                Q(last_name__icontains=search_query)
            )

        total_records = person_queryset.count()  # Total records before filtering

        # Apply sorting
        person_queryset = person_queryset.order_by(order_column)

        # Paginate results based on DataTables "start" and "length"
        paginator = Paginator(person_queryset, length)
        page_number = (start // length) + 1  # Convert offset to page number
        page_obj = paginator.get_page(page_number)

        data = list(
            page_obj.object_list.values(
                "id",
                "first_name",
                "last_name",
                "role",
            )
        )

        response = {
            "draw": draw,
            "recordsTotal": total_records,
            "recordsFiltered": total_records,
            "data": data
        }
        print("response", response)

        return JsonResponse(response)
