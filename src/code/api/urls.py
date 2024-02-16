from django.urls import path
from . import views

urlpatterns = [
    path('hello-world/', views.hello_world, name='hello_world'),
    path('list/', views.get_ten_books, name='get_ten_books'),
    path('filter-books/', views.filter_books, name='filter_books'),
    path('user-books/', views.user_books_list, name='user_books_list')
]