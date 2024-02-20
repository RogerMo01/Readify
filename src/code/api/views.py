import json
import os
import csv
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Runtime loaded data
all_books_data = []
indexed_books = {}
user_books = {}
user_book_list = {}
book_user_list = {}
l3 = set([])
readers = {}
readers_count = {}


# Data paths
csv_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'Books.csv')
csv_file_path = os.path.abspath(csv_file_path)

user_books_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'user_books.json')
user_books_path = os.path.abspath(user_books_path)

user_book_list_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'user_book_list.json')
user_book_list_path = os.path.abspath(user_book_list_path)

book_user_list_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'book_user_list.json')
book_user_list_path = os.path.abspath(book_user_list_path)

indexed_books_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'indexed_books.json')
indexed_books_path = os.path.abspath(indexed_books_path)

books_by_word_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'books_by_word.json')
books_by_word_path = os.path.abspath(books_by_word_path)


# Start load
print("⏳ Load started")
with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    all_books_data = list(csv_reader)

try:
    with open(user_books_path, 'r') as user_books_file:
        user_books = json.load(user_books_file)
except:
    user_books = {}
    with open(user_books_path, 'w') as user_books_file:
        json.dump(user_books, user_books_file, indent=2)

with open(user_book_list_path, 'r') as user_book_list_file:
    user_book_list = json.load(user_book_list_file)
with open(book_user_list_path, 'r') as book_user_list_file:
    book_user_list = json.load(book_user_list_file)
with open(indexed_books_path, 'r') as indexed_books_file:
    indexed_books = json.load(indexed_books_file)
with open(books_by_word_path, 'r') as books_by_word_file:
    books_by_word = json.load(books_by_word_file)
print("✅ Load end")



@api_view(['GET'])
def main_recommendation(request):
    # Main books recommender function
    
    readers = {}
    readers_count = {}
    l1 = list(map(lambda x : x[0], user_books.items()))
    l2 = set([])

    # Graph Search
    for b in l1:
        for u in book_user_list[b]:
            l2.add(u)
            for b2 in user_book_list[u]:
                try:
                    readers[b2].append(u)
                    readers_count[b2]+=1
                except:
                    l3.add(b2)
                    readers[b2] = [u]
                    readers_count[b2] = 0

    print(f'User spread to {len(l1)} books')
    print(f'l1 spread to {len(l2)} neighbors')
    print(f'l2 spread to {len(l3)} recommended books')


    ranked_set = list(sorted(l3, key=lambda x: readers_count.get(x, 0), reverse=True))

    # Limit ranked set to 10
    limited_ranked_set = []
    c = 0
    for b in ranked_set:
        if c == 10:
            break
        elif b not in user_books:
            limited_ranked_set.append(b)
            c+=1

    print('\n~~~~~~~~ Rank: ~~~~~~~~')
    for x in limited_ranked_set:
        print(f'{x} ({readers_count[x]} times)')

    request_response = list(map(lambda x: indexed_books[x], limited_ranked_set))

    return Response({'data': request_response})


@api_view(['GET'])
def filter_books(request):
    # Search for user query

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
    # List of user rated books
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