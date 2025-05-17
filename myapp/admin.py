from django.contrib import admin

from myapp.models import *

# Register your models here.

admin.site.register(Person)
admin.site.register(Publisher)
admin.site.register(Book)
# admin.site.register(BookPersonRole)
admin.site.register(Store)
# admin.site.register(StoreBook)