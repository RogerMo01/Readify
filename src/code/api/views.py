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
    ub = list(user_books.items())
    print(ub)

    count = 0
    response = []

    for book in all_books_data:
        if count == 10:
            break
        
        print(book['isbn'])
        if any(x[0] == book['isbn'] for x in ub):
            continue
        else:
            response.append(book)
            count+=1

    return Response({'data': response})

@api_view(['GET'])
def user_books_list(request):
    return Response({'data': list(user_books.items())})

@api_view(['POST'])
def add_book_to_user(request):
    try:
        data = json.loads(request.body.decode('utf-8'))

        isbn = data.get('isbn')
        title = data.get('bookTitle')
        author = data.get('bookAuthor')
        rating = "0.0"
        cover = data.get('imageURL_s')

        user_books[isbn] = {'rating': rating, 'title': title, 'author': author, 'cover': cover}

        # Save json
        with open(user_books_path, 'w') as user_books_file:
            json.dump(user_books, user_books_file, indent=2)

        return Response({'message': "OK"})
    except Exception as e:
        return Response({'message': str(e)}, status=400)