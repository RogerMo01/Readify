import json
import os
import csv
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

all_books_data = []
user_books = {}

# Cargar datos del CSV al inicio
csv_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'Books.csv')
csv_file_path = os.path.abspath(csv_file_path)

user_books_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'user_books.json')
user_books_path = os.path.abspath(user_books_path)

print("⏳ Load started")
with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    all_books_data = list(csv_reader)

with open(user_books_path, 'r') as user_books_file:
    user_books = json.load(user_books_file)
print("✅ Load end")


@api_view(['GET'])
def hello_world(request):
    return Response({'message': 'This is a message to confirm connection between Django and React'})

@api_view(['GET'])
def get_ten_books(request):
    return Response({'data': all_books_data[:10]})


@api_view(['GET'])
def filter_books(request):
    return Response({'data': all_books_data[:10]})

@api_view(['GET'])
def user_books_list(request):
    return Response({'data': list(user_books.items())})
