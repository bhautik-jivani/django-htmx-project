from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
ROLE_CHOICES = [
    ("A", _("Author")),
    ("E", _("Editor")),
]

class AuthorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role="A")


class EditorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role="E")


class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    role = models.CharField(max_length=1, choices=ROLE_CHOICES)
    
    objects = models.Manager()  # Default manager
    authors = AuthorManager()
    editors = EditorManager()
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.get_role_display()})"


class Publisher(models.Model):
    name = models.CharField(max_length=300)


class Book(models.Model):
    name = models.CharField(max_length=300)
    pages = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.FloatField()
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    pubdate = models.DateField()

    # Many-to-many relationship with a through model for roles
    persons = models.ManyToManyField(Person)


# class BookPersonRole(models.Model):
#     book = models.ForeignKey(Book, on_delete=models.CASCADE)
#     person = models.ForeignKey(Person, on_delete=models.CASCADE)
#     role = models.CharField(max_length=1, choices=ROLE_CHOICES)


class Store(models.Model):
    name = models.CharField(max_length=300)


class StoreBook(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    price_in_store = models.DecimalField(max_digits=10, decimal_places=2)
    stock_count = models.PositiveIntegerField()

