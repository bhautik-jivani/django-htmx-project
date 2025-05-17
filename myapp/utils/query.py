"""
Full Example: Creating All Models

from myapp.models import Person, Publisher, Book, BookPersonRole, Store, StoreBook

# 1. Create Persons (Author and Editor)
author = Person.objects.create(first_name="John", last_name="Doe", role="A")
editor = Person.objects.create(first_name="Jane", last_name="Smith", role="E")

# 2. Create Publisher
publisher = Publisher.objects.create(name="O'Reilly Media")

# 3. Create Book and link it to Publisher
book = Book.objects.create(
    name="Learning Django",
    pages=300,
    price=29.99,
    rating=4.7,
    publisher=publisher,
    pubdate="2023-05-01"
)

# 4. Link Author and Editor to the Book via BookPersonRole
BookPersonRole.objects.create(book=book, person=author, role="A")  # Author role
BookPersonRole.objects.create(book=book, person=editor, role="E")  # Editor role

# 5. Create Store
store = Store.objects.create(name="Local Bookstore")

# 6. Link Book to Store with additional information (price, stock)
StoreBook.objects.create(
    store=store,
    book=book,
    price_in_store=25.99,  # Price in store
    stock_count=100        # Stock available
)

print("All objects created successfully!")
"""


"""
Querying the Data
Once the data is created, you can query it like this:

To get all authors:
authors = Person.authors.all()


To get all editors:
editors = Person.editors.all()


To get all books linked to a particular store:
store = Store.objects.get(name="Local Bookstore")
books_in_store = store.books.all()


To get all persons associated with a book:
book = Book.objects.get(name="Learning Django")
persons_in_book = book.persons.all()


This should give you the basic CRUD operations for your models in Django. Let me know if you need further clarification!
"""