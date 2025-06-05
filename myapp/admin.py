from django.contrib import admin

from myapp.models import *

# Register your models here.

admin.site.register(Person)
admin.site.register(Publisher)
admin.site.register(Book)
# admin.site.register(BookPersonRole)
# admin.site.register(Store)
# admin.site.register(StoreBook)

class StoreBookInline(admin.TabularInline):
    model = StoreBook
    extra = 1
    min_num = 1
    max_num = 3

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)
    list_per_page = 10
    inlines = [StoreBookInline]

@admin.register(StoreBook)
class StoreBookAdmin(admin.ModelAdmin):
    list_display = ('store', 'book', 'price_in_store', 'stock_count')
    list_filter = ('store', 'book')
    search_fields = ('store__name', 'book__name')
    list_per_page = 10
