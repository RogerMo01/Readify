import os

from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
import csv

@api_view(['GET'])
def hello_world(request):
    return Response({'message': 'This is a message to confirm connection between Django and React'})

@api_view(['GET'])
def get_ten_books(request):

    parentDir = os.path.dirname(os.path.abspath(__file__))
    
    csv_file = os.path.join(parentDir, '..', '..', 'data', 'books_dataset.csv')
    csv_file = os.path.abspath(csv_file)

    data = []
    count = 0

    # Scan all books
    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        
        for book in csv_reader:

            if count >= 10:
                break
            
            data.append(book)
            count += 1

    return Response({'data': data})
