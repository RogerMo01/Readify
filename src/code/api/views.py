import json
import os
import csv
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Runtime loaded data
all_books_data = []
user_books = {}
user_book_list = {}
book_user_list = {}


# Data paths
csv_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'Books.csv')
csv_file_path = os.path.abspath(csv_file_path)

user_books_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'user_books.json')
user_books_path = os.path.abspath(user_books_path)

user_book_list_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'user_book_list.json')
user_book_list_path = os.path.abspath(user_book_list_path)

book_user_list_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'book_user_list.json')
book_user_list_path = os.path.abspath(book_user_list_path)


# Start load
print("⏳ Load started")
with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    all_books_data = list(csv_reader)
with open(user_book_list_path, 'r') as user_book_list_file:
    user_book_list = json.load(user_book_list_file)
with open(book_user_list_path, 'r') as book_user_list_file:
    book_user_list = json.load(book_user_list_file)
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

    count = 0
    response = []

    for book in all_books_data:
        if count == 10:
            break
        
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