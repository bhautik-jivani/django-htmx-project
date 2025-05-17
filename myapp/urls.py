from django.urls import path
from myapp import views

app_name = 'myapp'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard_view'),
    path('person/', views.PersonListView.as_view(), name='person_list_view'),
    path('person/create/', views.PersonCreateView.as_view(), name='person_create_view'),
    path('person/update/<int:pk>/', views.PersonUpdateView.as_view(), name='person_update_view'),

    path('publisher/', views.PublisherListView.as_view(), name='publisher_list_view'),
    path('publisher/create/', views.PublisherCreateView.as_view(), name='publisher_create_view'),
    path('publisher/update/<int:pk>/', views.PublisherUpdateView.as_view(), name='publisher_update_view'),

    path('book/', views.BookListView.as_view(), name='book_list_view'),
    path('book/create/', views.BookCreateView.as_view(), name='book_create_view'),
    path('book/update/<int:pk>/', views.BookUpdateView.as_view(), name='book_update_view'),

    path('add-person/', views.AddPersonFormView.as_view(), name='add_person_form_view'),
]
