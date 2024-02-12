from django.urls import path
from . import views

urlpatterns = [
    path('hello-world/', views.hello_world, name='hello_world'),
    path('list/', views.get_ten_books, name='get_ten_books')
]