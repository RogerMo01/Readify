from django.urls import path
from . import views

urlpatterns = [
    path('main-recommendation/', views.main_recommendation, name='main_recommendation'),
    path('filter-books/', views.filter_books, name='filter_books'),
    path('user-books/', views.user_books_list, name='user_books_list'),
    path('add-book/', views.add_book_to_user, name='add_book_to_user'),

]