# django libraries import
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Q, F, Sum, Case, When
from django.db import models
from django.views import View

# project models import
from myapp.models import Book  # Replace with your actual model

# Create your views here.
class BookAPIView(View):

    def get(self, request, *args, **kwargs):
        draw = int(request.GET.get("draw", 1))  # Required for DataTables
        search_query = request.GET.get("search[value]", "").strip()  # DataTables uses "search[value]"
        start = int(request.GET.get("start", 0))  # Offset for pagination
        length = int(request.GET.get("length", 10))  # Number of records per page

        print("request.GET", request.GET)
        order_column_index = int(request.GET.get("order[0][column]", 1))  # Default to column index 1
        order_dir = request.GET.get("order[0][dir]", "asc")

        # Mapping DataTables column index to model field names
        column_mapping = {
            0: "id",
            1: "name",
            2: "pages",
            3: "price",
            4: "rating",
            5: "publisher",
            6: "pubdate",
        }

        # Default sorting column
        order_column = column_mapping.get(order_column_index, "id")

        # Apply sorting direction
        if order_dir == "desc":
            order_column = f"-{order_column}"  # Add '-' for descending order

        if length > 50:  # Enforce max limit
            length = 50

        # Apply search filter (adjust fields based on your model)
        book_queryset = Book.objects.all()
        if search_query:
            book_queryset = book_queryset.filter(
                Q(id__icontains=search_query) | 
                Q(name__icontains=search_query) |
                Q(pages__icontains=search_query) |
                Q(price__icontains=search_query) |
                Q(rating__icontains=search_query) |
                Q(publisher__name__icontains=search_query) |
                Q(pubdate__icontains=search_query)
            )

        total_records = book_queryset.count()  # Total records before filtering

        # Apply sorting
        book_queryset = book_queryset.order_by(order_column)

        # Paginate results based on DataTables "start" and "length"
        paginator = Paginator(book_queryset, length)
        page_number = (start // length) + 1  # Convert offset to page number
        page_obj = paginator.get_page(page_number)

        data = [
            {
                "id": book.id,
                "name": book.name,
                "pages": book.pages,
                "price": book.price,
                "rating": book.rating,
                "publisher": book.publisher.name,
                "pubdate": book.pubdate,
            }
            for book in page_obj.object_list
        ]

        response = {
            "draw": draw,
            "recordsTotal": total_records,
            "recordsFiltered": total_records,
            "data": data
        }

        return JsonResponse(response)
